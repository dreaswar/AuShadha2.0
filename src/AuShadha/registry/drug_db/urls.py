from django.urls import re_path
from django.contrib import admin
import AuShadha.settings
admin.autodiscover()

from .views import fda_drug_db_json_all_drugs,  \
                   fda_drug_db_json_for_a_drug, \
                   fda_drug_db_search,          \
                   fda_drug_db_advanced_search, \
                   fda_drug_summary

from .dijit_widgets.pane import render_fda_drug_db_pane
from .dijit_widgets.tree import render_fda_drug_db_tree


urlpatterns = [
        
	re_path(r'drug_db/pane/$', render_fda_drug_db_pane, name = 'drug_db_pane'),
	re_path(r'render/pane/$', render_fda_drug_db_pane, name = 'render_fda_drug_db_pane'),
	re_path(r'render/tree/$', render_fda_drug_db_tree, name = 'render_fda_drug_db_tree'),

	re_path(r'fda_drug_db/json/all_drugs/$', 
            fda_drug_db_json_all_drugs, 
            name = 'fda_drug_db_json_all_drugs'
          ),

	re_path(r'fda_drug_db/json_for_a_drug/(?P<drug_id>\d+)/$', 
            fda_drug_db_json_for_a_drug, 
            name = 'fda_drug_db_json_for_a_drug'
          ),

	re_path(r'fda_drug/summary/(?P<drug_id>\d+)/$', 
            fda_drug_summary, 
            name = 'fda_drug_summary'
          ),

	re_path(r'fda_drug_db/search/$', 
            fda_drug_db_search,
            name = 'fda_drug_db_search'
          ),

	re_path(r'fda_drug_db/advanced_search/$', 
            fda_drug_db_advanced_search, 
            name = 'fda_drug_db_advanced_search'
         )

]


