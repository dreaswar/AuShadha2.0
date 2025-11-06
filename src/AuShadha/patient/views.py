# -*- coding: utf-8 -*-

########################################################
# MODULE  : Views for Patient Management
# PROJECT : Part of AuShadha2.0 Open Source EMR
# LICENSE : GNU GPL Version3.0
# Author  : Dr. Easwar T.R
# Date    : 13-09-2018
########################################################

########################### General Module imports #############################

import json
import logging
from datetime import datetime, date, time

########################### General Django Imports #############################

from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings

##################### Application Specific Model Imports #######################

from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree
from AuShadha.utilities.forms import aumodelformerrorformatter_factory

from aushadha_ui.data.json import ModelInstanceJson
from aushadha_ui.data.summary import ModelInstanceSummary
from aushadha_ui.ui import ui as UI

# Initialize logger
logger = logging.getLogger(__name__)

# Get APP_ROOT_URL from settings
APP_ROOT_URL = getattr(settings, 'APP_ROOT_URL', '/AuShadha/')


######################### Helper Functions #######################################

def is_ajax(request):
    """
    Check if request is AJAX (Django 4.0+ compatible).
    Replaces deprecated request.is_ajax()
    """
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'




######################### Views start here ######################################


from clinic.models import Clinic
from patient.models import PatientDetail, PatientDetailForm
from .dijit_widgets.tree import PatientTree


######################### HTMX VIEWS (NEW) #######################################

@login_required
def patient_home(request):
    """
    Patient home page with HTMX-powered list.
    Main landing page for patient management.
    """
    return render(request, 'patient/home.html', {
        'user': request.user,
    })


@login_required
def patient_list(request):
    """
    Patient list partial - loaded via HTMX.
    Supports search and pagination.
    """
    from django.core.paginator import Paginator

    # Get search query
    search_query = request.GET.get('search', '').strip()

    # Base queryset
    patients = PatientDetail.objects.select_related('parent_clinic').all()

    # Apply search filter
    if search_query:
        from django.db.models import Q
        patients = patients.filter(
            Q(patient_hospital_id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(middle_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(full_name__icontains=search_query)
        )

    # Order by most recent first
    patients = patients.order_by('-id')

    # Pagination
    paginator = Paginator(patients, 20)  # 20 patients per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'patients': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'search_query': search_query,
    }

    return render(request, 'patient/partials/patient_list.html', context)


@login_required
def patient_detail(request, id):
    """
    Patient detail view - loaded via HTMX.
    Shows comprehensive patient information.
    """
    try:
        patient = PatientDetail.objects.select_related('parent_clinic').get(pk=id)
    except PatientDetail.DoesNotExist:
        return HttpResponse(
            '<div class="alert alert-error">Patient not found</div>',
            status=404
        )

    context = {
        'patient': patient,
        'user': request.user,
    }

    return render(request, 'patient/partials/patient_detail.html', context)


######################### ORIGINAL VIEWS ##########################################


@login_required
def render_patient_json(request):


    if request.method == 'GET':
        all_p = PatientDetail.objects.all()
        if all_p is not None:
            data = []
            for patient in all_p:
                logger.debug(f"Evaluating Patient: {patient}")
                jsondata = ModelInstanceJson(patient).return_data()
                data.append(jsondata)
        else:
            data = {}
        jsondata = json.dumps(data)
        return HttpResponse(jsondata, content_type="application/json")
    else:
        raise Http404("Bad Request Method")


@login_required
def render_patient_summary(request, patient_id=None):
    if request.method == "GET" and is_ajax(request):
        user = request.user

        if patient_id:
            patient_id = int(patient_id)
        else:
            patient_id = int(request.GET.get('patient_id'))


      #  try:
        pat_obj = PatientDetail.objects.get(pk=patient_id)
        var = ModelInstanceSummary(pat_obj).variable
        var['user'] = user
        return render(request, 'patient_detail/summary.html', var)

        #except(AttributeError, NameError, KeyError, TypeError, ValueError):
         #   raise Http404("ERROR! Bad Request Parameters")

        #except(AttributeError, NameError, KeyError, TypeError, ValueError):
         #   raise Http404("ERROR! Requested Patient Data Does not exist")
    else:
        raise Http404("Bad Request")


@login_required
def render_patient_info(request, patient_id=None):
    if request.user and request.method == 'GET':
        if patient_id:
            try:
                patient_id = int(patient_id)
                patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
            except (NameError, ValueError, TypeError, AttributeError):
                raise Http404("Bad Request Parameters")
            except(PatientDetail.DoesNotExist):
                raise Http404("Requested Patient Does Not Exist")
            # data = {'success': True,
                # 'error_message': 'Successfully retrieved patient info',
                # 'info': patient_detail_obj.__unicode__()
                # }
            #jsondata = json.dumps(data)
            # return HttpResponse(jsondata, content_type='application/json')
            variable = {'info': patient_detail_obj}

            return render(request, 'patient_detail/info.html', variable)
    else:
        return HttpResponseRedirect('login')


@login_required
def patient_detail_add(request, clinic_id=None):

    user = request.user
    logger.info("Received request to add new patient")

    try:
        if clinic_id:
            clinic_id = int(clinic_id)
        else:
            clinic_id = int(request.GET.get('clinic_id'))
    except (KeyError, NameError, AttributeError, ValueError, TypeError):
        clinic_id = 1

    try:
        clinic = Clinic.objects.get(pk=clinic_id)
        patient_detail_obj = PatientDetail(parent_clinic=clinic)
        if request.method == "GET":
            patient_detail_form = PatientDetailForm(
                instance=patient_detail_obj)
            variable = {"user": user,
                        "patient_detail_obj": patient_detail_obj,
                        "patient_detail_form": patient_detail_form
                        }

            # Return form partial for HTMX
            if is_ajax(request):
                return render(request, 'patient/partials/patient_form.html', variable)
            # Or full page for non-AJAX
            return render(request, 'patient_detail/add.html', variable)

        elif request.method == "POST" and is_ajax(request):
            patient_detail_form = PatientDetailForm(request.POST,
                                                    instance=patient_detail_obj)
            if patient_detail_form.is_valid():
                saved_patient = patient_detail_form.save(commit=False)
                saved_patient.parent_clinic = clinic
                saved_patient.save()
                success = True
                error_message = "Patient Saved Successfully"
                form_errors = None
                #jsondata = return_patient_json(saved_patient,success)
            else:
                form_errors = aumodelformerrorformatter_factory(
                    patient_detail_form)
                saved_patient = None
                success = False
            data = {'success': success,
                    'error_message': form_errors,
                    'form_errors': form_errors
                    }
            jsondata = json.dumps(data)

        else:
            raise Http404('Bad Request:: Unsupported Request Method.')

    except(Clinic.DoesNotExist):
        saved_patient = None
        success = False

        data = {'success': success,
                'error_message': "No Clinic by the specified id"}
        jsondata = json.dumps(data)

    return HttpResponse(jsondata, content_type='application/json')



@login_required
def patient_detail_edit(request, id):
    """
    Edit patient details - supports both HTMX and traditional requests.
    """
    if not request.user:
        return HttpResponseRedirect('login')

    user = request.user

    try:
        id = int(id)
        patient_detail_obj = PatientDetail.objects.get(pk=id)
        if not getattr(patient_detail_obj, 'urls', None):
            patient_detail_obj.save()

    except (TypeError, ValueError, AttributeError):
        logger.error(f"Invalid patient ID: {id}")
        raise Http404("BadRequest")

    except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Patient detail Data Does Not Exist")

    if request.method == "GET":
        patient_detail_edit_form = PatientDetailForm(
            auto_id=False, instance=patient_detail_obj)
        variable = {
            "user": user,
            "patient": patient_detail_obj,  # For HTMX template
            "patient_detail_obj": patient_detail_obj,  # For legacy template
            "patient_detail_edit_form": patient_detail_edit_form
        }

        # Return edit partial for HTMX
        if is_ajax(request):
            return render(request, 'patient/partials/patient_edit.html', variable)
        # Or full page for non-AJAX
        return render(request, 'patient_detail/edit.html', variable)

    elif request.method == 'POST':
        patient_detail_edit_form = PatientDetailForm(
            request.POST, instance=patient_detail_obj)

        if patient_detail_edit_form.is_valid():
            detail_object = patient_detail_edit_form.save()
            logger.info(f"Patient {detail_object.patient_hospital_id} updated successfully")

            # For HTMX, return updated patient list
            if is_ajax(request):
                # Refresh the patient list
                return patient_list(request)
            else:
                # For non-AJAX, return JSON
                data = {
                    'success': True,
                    'error_message': 'Patient Edited Successfully',
                    'form_errors': None
                }
                return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            logger.warning(f"Patient edit form validation failed: {patient_detail_edit_form.errors}")

            # For HTMX, return form with errors
            if is_ajax(request):
                variable = {
                    "user": user,
                    "patient": patient_detail_obj,
                    "patient_detail_obj": patient_detail_obj,
                    "patient_detail_edit_form": patient_detail_edit_form
                }
                return render(request, 'patient/partials/patient_edit.html', variable)
            else:
                # For non-AJAX, return JSON with errors
                form_errors = ''
                for error in patient_detail_edit_form.errors:
                    form_errors += f'<p>{error}</p>'

                data = {
                    'success': False,
                    'error_message': 'Error: Patient Detail could not be edited.',
                    'form_errors': form_errors
                }
                return HttpResponse(json.dumps(data), content_type='application/json')

    else:
        raise Http404("BadRequest: Unsupported Request Method")


@login_required
def patient_detail_del(request, id):
    """
    Delete patient - supports both HTMX DELETE and traditional GET requests.
    Only superusers can delete patients.
    """
    user = request.user

    # Check superuser permission
    if not user.is_superuser:
        logger.warning(f"User {user.username} attempted to delete patient without permissions")
        if is_ajax(request):
            return HttpResponse(
                '<div class="alert alert-error">You do not have permission to delete patients.</div>',
                status=403
            )
        else:
            raise Http404("Server Error: No Permission to delete.")

    # Support both DELETE (HTMX) and GET (legacy) methods
    if request.method not in ["GET", "DELETE"]:
        raise Http404("BadRequest: Unsupported Request Method")

    try:
        id = int(id)
        patient_detail_obj = PatientDetail.objects.get(pk=id)
    except (TypeError, ValueError, AttributeError):
        logger.error(f"Invalid patient ID for deletion: {id}")
        if is_ajax(request):
            return HttpResponse(
                '<div class="alert alert-error">Invalid patient ID. Please refresh and try again.</div>',
                status=400
            )
        else:
            raise Http404("BadRequest")
    except PatientDetail.DoesNotExist:
        logger.error(f"Patient with ID {id} not found for deletion")
        if is_ajax(request):
            return HttpResponse(
                '<div class="alert alert-error">Patient not found. They may have already been deleted.</div>',
                status=404
            )
        else:
            raise Http404("BadRequest: Patient detail Data Does Not Exist")

    # Perform deletion
    patient_name = patient_detail_obj.full_name or patient_detail_obj.first_name
    patient_detail_obj.delete()
    logger.info(f"Patient {patient_name} (ID: {id}) deleted by {user.username}")

    # Return appropriate response
    if is_ajax(request):
        # For HTMX, return empty response with success header
        # The hx-swap="outerHTML swap:1s" in the template will handle the animation
        return HttpResponse('', status=200)
    else:
        # Legacy JSON response
        data = {
            "success": True,
            "error_message": "Patient Deleted Successfully"
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
