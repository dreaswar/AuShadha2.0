# -*- coding: utf-8 -*-
##########################################################################
# Project: AuShadha
# Description: Pane of the UI
# Author ; Dr.Easwar T.R
# Date: 04-11-2013
# License: GNU-GPL Version3, see LICENSE.txt for details
##########################################################################

import yaml
from io import StringIO

# General Django Imports----------------------------------
from django.http import Http404, HttpResponse
import json
from django.urls import reverse
from django.template import RequestContext
from django.template import Template, Context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from aushadha_ui.ui import ui as UI


@login_required
def render_icd10pcs_pane(request):

    if request.method != 'GET':
        raise Http404("Bad Request Method")

    user = request.user
    app_wrapper = []
    context = RequestContext(request, {'user': user})
    try:
        pane_template = Template(
            open(
                'registry/icd10pcs/dijit_widgets/pane.yaml',
                'r').read())
    except(IOError):
        raise Http404("No template file to render the pane ! ")
    rendered_pane = pane_template.render(context)
    pane_yaml = yaml.load(rendered_pane)

    app_object = {}
    app_object['app'] = 'ICD10_PCS'
    app_object['ui_sections'] = {
        'app_type': 'sub_module',
        'load_after': 'patient',
        'load_first': False,
        'layout': ['trailing', 'top', 'center'],
        'widgets': {
            'tree': None,
            'summary': None,
            'grid': None,
            'search': None
        }
    }
    app_object['url'] = ''
    app_wrapper.append(app_object)

    success = True
    error_message = "Returning ICD10 app pane variables"

    data = {
        'success': success,
        'error_message': error_message,
        'app': app_wrapper,
        'pane': pane_yaml
    }
    jsondata = json.dumps(data)
    return HttpResponse(jsondata, content_type="application/json")
