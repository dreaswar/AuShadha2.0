"""AuShadha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import absolute_import
from __future__ import print_function
from django.conf.urls import url , include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views 

from AuShadha import settings
from aushadha_users.views import login_view, logout_view


from .startup import run

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^AuShadha/search/', include('search.urls') ),

    url(r'^home/', include('aushadha_ui.urls') ),
    url(r'^AuShadha/home/', include('aushadha_ui.urls') ),
    url(r'^AuShadha/ui/', include('aushadha_ui.urls') ),
    # url(r'^$', include('aushadha_ui.urls'))

    url(r'^AuShadha/authenticate/', include('aushadha_users.urls')),

    #    url(r'^AuShadha/logout/$', include('aushadha_users.urls')),


  url(r'^AuShadha/icd10/'  , include('registry.icd10.urls') ),
  url(r'^AuShadha/icd10pcs/' , include('registry.icd10pcs.urls') ),
  url(r'^AuShadha/drug_db/'  , include('registry.drug_db.urls') ),
  url(r'^AuShadha/fda_drug_db/', include('registry.drug_db.urls') ),
  url(r'^AuShadha/drugbankcadrugs/', include('registry.drug_db.drugbankca.urls') ),


  url(r'^AuShadha/pat/'    , include('patient.urls') ),
  url(r'^AuShadha/patient/', include('patient.urls') ),
  url(r'^AuShadha/patient/', include('patient.urls') ),

# url(r'^AuShadha/admission/', include('admission.admission.urls') ),
# url(r'^AuShadha/demographics/', include('demographics.demographics.urls') ),
# url(r'^AuShadha/contact/'     , include('demographics.contact.urls') ),
# url(r'^AuShadha/phone/'       , include('demographics.phone.urls') ),
# url(r'^AuShadha/guardian/'    , include('demographics.guardian.urls') ),
# url(r'^AuShadha/email_and_fax/',include('demographics.email_and_fax.urls') ),
# url(r'^AuShadha/family_history/'  , include('history.family_history.urls')),
# url(r'^AuShadha/social_history/'  , include('history.social_history.urls')),
# url(r'^AuShadha/medical_history/' , include('history.medical_history.urls')),
# url(r'^AuShadha/surgical_history/', include('history.surgical_history.urls')),
# url(r'^AuShadha/obs_and_gyn/'    , include('history.obs_and_gyn.urls') ),
# url(r'^AuShadha/medication_list/', include('medication_list.urls') ),
# url(r'^AuShadha/allergy_list/'   , include('allergy_list.urls') ),
# url(r'^AuShadha/immunisation/'   , include('immunisation.urls') ),

# url(r'^AuShadha/visit/'             , include('visit.visit.urls')),
# url(r'^AuShadha/visit_complaint/'   , include('visit.visit_complaints.urls') ),
# url(r'^AuShadha/visit_complaints/'  , include('visit.visit_complaints.urls') ),
# url(r'^AuShadha/visit_hpi/'         , include('visit.visit_hpi.urls') ),
# url(r'^AuShadha/visit_ros/'         , include('visit.visit_ros.urls') ),
# url(r'^AuShadha/visit_phyexam/'     , include('visit.visit_phyexam.urls') ),
# url(r'^AuShadha/visit_assessment_and_plan/',include('visit.visit_assessment_and_plan.urls') ),
# url(r'^AuShadha/visit_soap/' , include('visit.visit_soap.urls') ),
# url(r'^AuShadha/visit_prescription/',include('visit.visit_prescription.urls') ),

# url(r'^AuShadha/follow_up/', include('visit.urls')),
# url(r'^AuShadha/phyexam/'  , include('phyexam.urls')),

# Admin and Admin Docs URL:
#   url(r'^AuShadha/admin/', include(admin.site.urls)),
#   url(r'^AuShadha/admin/doc/', include('django.contrib.admindocs.urls')),

# Media URL
# url( r'^AuShadha/media/(?P<path>.*)$', 
#        'django.views.static.serve',
#        {'document_root': settings.MEDIA_ROOT}, 
#        'show_indexes:True'
#        ),

# Home URL
# TODO This will be the true address.. a kind of like a Dashboard. 
#      Till then use the one below for /AuShadha/home/
#(r'^AuShadha/home/$', 'home.views.home'),
#(r'^AuShadha/home/$', 'patient.views.patient_list'),

# Login and Logout URLS
    #url(r'^AuShadha/log/', include('aushadha_users.urls') ),
    #url(r'^AuShadha/logout/$',include('aushadha_users.urls') ),
    url(r'^AuShadha/authenticate/', include('aushadha_users.urls') ),

#url(r'^AuShadha/login/$', login_view, name="login"),
#url(r'^AuShadha/logout/$',logout_view, name="logout"),

# If it dosent match anything else..
#(r'^AuShadha/alternate_layout/$','patient.views.alternate_layout'),
#(r'^AuShadha/$', 'patient.views.patient_list'),
#(r'^$', 'patient.views.patient_list'),
# url(r'^AuShadha/', include('aushadha_ui.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()

#print(urlpatterns)




# Right now Django does not allow custom statup code to run anywhere 
# So if we want to run code after AppRgistry.ready<Bool> this is the safe
# place 
run() 

