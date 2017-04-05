
########################### General Module imports #############################

from __future__ import absolute_import
from __future__ import print_function
from datetime import datetime, date, time
import json

########################### General Django Imports #############################

from django.shortcuts import render_to_response
from django.shortcuts import render

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
#from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required




######################### Views start here ######################################


@login_required
def render_patient_json(request):

    if request.method =='GET':
      all_p = PatientDetail.objects.all()
      if all_p is not None:
          data = []
          for patient in all_p:
              print("Evaluating Patient: ")
              print(patient)
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
    if request.method == "GET" and request.is_ajax():
        user = request.user

        if patient_id:
            patient_id = int(patient_id)
        else:
            patient_id = int(request.GET.get('patient_id'))

        try:
            pat_obj = PatientDetail.objects.get(pk=patient_id)
            var = ModelInstanceSummary(pat_obj).variable
            var['user']  = user
            variable = RequestContext(request, var)
            return render_to_response('patient_detail/summary.html', variable)

        except(AttributeError, NameError, KeyError, TypeError, ValueError):
            raise Http404("ERROR! Bad Request Parameters")

        except(AttributeError, NameError, KeyError, TypeError, ValueError):
            raise Http404("ERROR! Requested Patient Data Does not exist")
    else:
        raise Http404("Bad Request")

@login_required
def render_patient_info(request,patient_id = None):
  if request.user and request.method == 'GET':
    if patient_id:
      try:
        patient_id = int( patient_id )
        patient_detail_obj = PatientDetail.objects.get(pk = patient_id )
      except (NameError,ValueError,TypeError,AttributeError):
        raise Http404("Bad Request Parameters")
      except(PatientDetail.DoesNotExist):
        raise Http404("Requested Patient Does Not Exist")
      #data = {'success': True,
              #'error_message': 'Successfully retrieved patient info',
              #'info': patient_detail_obj.__unicode__()
              #}
      #jsondata = json.dumps(data)
      #return HttpResponse(jsondata, content_type='application/json')
      variable = RequestContext(request,
                                {'info': patient_detail_obj}
                                )
      return render_to_response( 'patient_detail/info.html', variable )
  else:
    return HttpResponseRedirect('login')


@login_required
def patient_detail_add(request, clinic_id = None):

    user = request.user
    print("Received a request to add a New Patient....")

    try:
      if clinic_id :
        clinic_id = int(clinic_id)
      else:
        clinic_id = int(request.GET.get('clinic_id'))
    except (KeyError,NameError,AttributeError,ValueError,TypeError):
        clinic_id = 1

    try:
      clinic = Clinic.objects.get(pk = clinic_id)
      patient_detail_obj = PatientDetail(parent_clinic = clinic)
      if request.method == "GET" and request.is_ajax():
          patient_detail_form = PatientDetailForm(
              instance=patient_detail_obj)
          variable = RequestContext(request,
                                    {"user": user,
                                    "patient_detail_obj": patient_detail_obj,
                                    "patient_detail_form": patient_detail_form
                                    }
                                    )
          return render_to_response('patient_detail/add.html', variable)

      elif request.method == "POST"  and request.is_ajax():
          patient_detail_form = PatientDetailForm(request.POST,
                                                  instance = patient_detail_obj)
          if patient_detail_form.is_valid():
              saved_patient = patient_detail_form.save(commit = False)
              saved_patient.parent_clinic = clinic
              saved_patient.save()
              success = True
              error_message = "Patient Saved Successfully"
              form_errors = None
              #jsondata = return_patient_json(saved_patient,success)
          else:
              form_errors = aumodelformerrorformatter_factory(patient_detail_form)
              saved_patient = None
              success = False
          data = {'success':success,
                  'error_message':form_errors,
                  'form_errors': form_errors
                  }
          jsondata = json.dumps(data)

      else:
          raise Http404('Bad Request:: Unsupported Request Method.')

    except(Clinic.DoesNotExist):
        saved_patient = None
        success = False
        data = {'success':success,'error_message':"No Clinic by the specified id"}
        jsondata = json.dumps(data)

    return HttpResponse(jsondata, content_type='application/json')




@login_required

def patient_detail_edit(request, id):

    if request.user:
        user = request.user
        try:
            id = int(id)
            patient_detail_obj = PatientDetail.objects.get(pk=id)
            if not getattr(patient_detail_obj,'urls',None):
              patient_detail_obj.save()

        except TypeError or ValueError or AttributeError:
            raise Http404("BadRequest")

        except PatientDetail.DoesNotExist:
            raise Http404("BadRequest: Patient detail Data Does Not Exist")

        if request.method == "GET" and request.is_ajax():
            patient_detail_edit_form = PatientDetailForm(auto_id = False, instance=patient_detail_obj)
            variable = RequestContext(request,
                                      {"user"   : user,
                                        "patient_detail_obj" : patient_detail_obj,
                                        "patient_detail_edit_form"   : patient_detail_edit_form
                                        }
                                      )
            return render_to_response('patient_detail/edit.html', variable)

        elif request.method == 'POST' and request.is_ajax():
            patient_detail_edit_form = PatientDetailForm(request.POST, instance=patient_detail_obj)
            if patient_detail_edit_form.is_valid():
                detail_object = patient_detail_edit_form.save()
                success = True
                error_message = "Patient Edited Successfully"
                form_errors = None
                #jsondata = return_patient_json(detail_object, success=True)
            else:
                success = False
                error_message = "Error:: Patient Detail could not be edited."
                form_errors = ''
                for error in patient_detail_edit_form.errors:
                    form_errors += '<p>' + error + '</p>'
                #jsondata = return_patient_json(detail_object=None, success=False)
            data  = {'success': success,
                     'error_message': error_message,
                     'form_errors': form_errors
                    }
            jsondata = json.dumps(data)
            return HttpResponse(jsondata, content_type='application/json')

        else:
            raise Http404("BadRequest: Unsupported Request Method")


@login_required
def patient_detail_del(request, id):
    user = request.user
    if request.user and user.is_superuser:
        if request.method == "GET":
            try:
                id = int(id)
                patient_detail_obj = PatientDetail.objects.get(pk=id)
            except TypeError or ValueError or AttributeError:
                if request.is_ajax():
                    success = False
                    error_message = '''
                            ERROR!! Bad Request. Please refresh page and try again.
                           '''
                    data = {"success": success, "error_message": error_message}
                    jsondata = json.dumps(data)
                    return HttpResponse(jsondata, content_type="application/json")
                else:
                    raise Http404("BadRequest")
            except PatientDetail.DoesNotExist:
                if request.is_ajax():
                    success = False
                    error_message = '''
                            ERROR!! Requested Patient Data Does not Exist.
                            Refresh Page and try again..
                           '''
                    data = {"success": success, "error_message": error_message}
                    jsondata = json.dumps(data)
                    return HttpResponse(jsondata, content_type="application/json")
                else:
                    raise Http404(
                        "BadRequest: Patient detail Data Does Not Exist")
            if user.is_superuser:
                patient_detail_obj.delete()
                if request.is_ajax():
                    success = True
                    error_message = "Patient Deleted Successfully"
                    data = {"success": success, "error_message": error_message}
                    jsondata = json.dumps(data)
                    return HttpResponse(jsondata, content_type="application/json")
                else:
                    return HttpResponseRedirect('/')
            else:
                if request.is_ajax():
                    success = False
                    error_message = "ERROR ! No Priviliges to Delete..."
                    data = {"success": success, "error_message": error_message}
                    jsondata = json.dumps(data)
                    return HttpResponse(jsondata, content_type="application/json")
                else:
                    return HttpResponseRedirect('/')
        else:
            raise Http404("BadRequest: Unsupported Request Method")
    else:
        raise Http404("Server Error: No Permission to delete.")