from __future__ import absolute_import
from django.urls import re_path, include
#from django.views.generic.simple import direct_to_template

import AuShadha.settings

from .views import aushadha_patient_search
from .dijit_widgets.pane import render_aushadha_search_pane, render_aushadha_search_form

urlpatterns = [
  re_path(r'patient/$',
      aushadha_patient_search,
      name='aushadha_patient_search'
  ),
  re_path(r'patient/(?P<patient_id>\d+)/$',
      aushadha_patient_search,
      name='aushadha_patient_search_with_id'
  ),
  re_path(r'pane/$',
      render_aushadha_search_pane,
      name='render_aushadha_search_pane'
  ),
  re_path(r'render/form/$',
      render_aushadha_search_form,
      name='render_aushadha_search_form'
  ),
] 
