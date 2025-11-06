from django.urls import re_path
from django.contrib import admin
import AuShadha.settings

from .views import *
from .dijit_widgets.pane import render_patient_pane
from .dijit_widgets.tree import render_patient_tree

admin.autodiscover()

urlpatterns = [ 

################################ PATIENT CRUD ##################################

   re_path(r'new/add/(?P<clinic_id>\d+)/$'                             ,
       patient_detail_add,
       name='patient_detail_add'
       ),

   re_path(r'new/add/$'                             ,
       patient_detail_add,
       name='patient_detail_add_without_id'
       ),

   re_path(r'patient/edit/(?P<id>\d+)/$',
       patient_detail_edit,
       name='patient_detail_edit'
       ),

   re_path(r'patient/del/(?P<id>\d+)/$',
       patient_detail_del,
       name='patient_detail_del'
       ),


################################ PATIENT JSON ##################################

   re_path(r'patient/json/$',
           render_patient_json,
           name='render_patient_json'
       ),


################################ PATIENT SUMMARY ###############################

   re_path(r'patient/summary/$',
       render_patient_summary,
       name='render_patient_summary_without_id'
       ),

   re_path(r'patient/summary/(?P<patient_id>\d+)/$',
       render_patient_summary,
       name='render_patient_summary_with_id'
       ),

################################ PATIENT INFO  #################################

  re_path(r'patient/info/(?P<patient_id>\d+)/$',
       render_patient_info,
       name='render_patient_info'
       ),

################################ PATIENT PANE ##################################

  re_path(r'patient/pane/(?P<patient_id>\d+)/$',
       render_patient_pane,
       name='render_patient_pane_with_id'
       ),

  re_path(r'patient/pane/$',
       render_patient_pane,
       name='render_patient_pane_without_id'
       ),

################################ PATIENT TREE ##################################

   re_path(r'patient/tree/(?P<patient_id>\d+)/$',
       render_patient_tree,
       name='render_patient_tree_with_id'
       ),

   re_path(r'patient/tree/$',
       render_patient_tree,
       name='render_patient_tree_without_id'
       ),

############################ PATIENT INDEX ######################################

   #url(r'patient/index/$',
       #'patient.views.patient_index',
       #name='patient_index'
       #),

############################ PATIENT LIST ######################################

   #url(r'patient/list/$',
       #'patient.views.render_patient_list' ,
       #name='render_patient_list'
       #),

   #    url(r'patient/list/(?P<id>\d+)/$',
   #            'patient.views.patient_detail_list',
   #            name = 'patient_detail_list'
   #    ),

]
