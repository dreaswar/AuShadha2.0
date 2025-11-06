# -*- coding: utf-8 -*-

from django.urls import re_path
from django.contrib import admin

import AuShadha.settings

admin.autodiscover()

from .views import icd10pcs_code_search
from .dijit_widgets.pane import render_icd10pcs_pane
from .dijit_widgets.tree import render_axis_tree

urlpatterns = [
    re_path(r'render/pane/$', 
        render_icd10pcs_pane, 
        name = 'render_icd10_pcs_pane'),
    re_path(r'icd10pcs/pane/$', 
        render_icd10pcs_pane, 
        name = 'icd10_pcs_pane'),
    re_path(r'render/axis/tree/(?P<codepage>\*|\w*)/(?P<pos>\d)/$', 
        render_axis_tree, 
        name = 'render_axis_tree'),
    re_path(r'code/search/$', 
        icd10pcs_code_search, 
        name = 'icd10pcs_code_search'),
]


