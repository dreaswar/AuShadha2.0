"""
URL Configuration for Patient Module
Django 4.2 compatible with path() syntax
"""

from django.urls import path
from django.contrib import admin

from . import views
from .dijit_widgets.pane import render_patient_pane
from .dijit_widgets.tree import render_patient_tree

app_name = 'patient'

urlpatterns = [

    ################################ HTMX VIEWS (NEW) ###############################

    # Patient Home (list page)
    path('', views.patient_home, name='patient_home'),

    # Patient List (HTMX partial)
    path('list/', views.patient_list, name='patient_list'),

    # Patient Detail (HTMX partial)
    path('<int:id>/detail/', views.patient_detail, name='patient_detail'),

    ################################ PATIENT CRUD ##################################

    # Add Patient
    path('add/', views.patient_detail_add, name='patient_add'),
    path('add/<int:clinic_id>/', views.patient_detail_add, name='patient_add_with_clinic'),

    # Edit Patient
    path('<int:id>/edit/', views.patient_detail_edit, name='patient_edit'),

    # Delete Patient
    path('<int:id>/delete/', views.patient_detail_del, name='patient_delete'),

    ################################ PATIENT JSON ##################################

    path('json/', views.render_patient_json, name='render_patient_json'),

    ################################ PATIENT SUMMARY ###############################

    path('summary/', views.render_patient_summary, name='render_patient_summary_without_id'),
    path('<int:patient_id>/summary/', views.render_patient_summary, name='render_patient_summary_with_id'),

    ################################ PATIENT INFO  #################################

    path('<int:patient_id>/info/', views.render_patient_info, name='render_patient_info'),

    ################################ PATIENT PANE ##################################

    path('pane/', render_patient_pane, name='render_patient_pane_without_id'),
    path('<int:patient_id>/pane/', render_patient_pane, name='render_patient_pane_with_id'),

    ################################ PATIENT TREE ##################################

    path('tree/', render_patient_tree, name='render_patient_tree_without_id'),
    path('<int:patient_id>/tree/', render_patient_tree, name='render_patient_tree_with_id'),

]
