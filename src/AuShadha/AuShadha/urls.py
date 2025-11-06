"""
AuShadha URL Configuration - Django 4.2 Compatible

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),

    # Main application home - redirect to patients
    path('', RedirectView.as_view(url='/AuShadha/patients/', permanent=False)),
    path('AuShadha/', RedirectView.as_view(url='/AuShadha/patients/', permanent=False)),

    # Authentication
    path('AuShadha/authenticate/', include('aushadha_users.urls')),
    path('login/', RedirectView.as_view(url='/AuShadha/authenticate/login/', permanent=False), name='login'),
    path('logout/', RedirectView.as_view(url='/AuShadha/authenticate/logout/', permanent=False), name='logout'),

    # Core modules
    path('AuShadha/patients/', include('patient.urls')),  # Main patient module
    path('AuShadha/search/', include('search.urls')),
    path('AuShadha/ui/', include('aushadha_ui.urls')),
    path('AuShadha/home/', include('aushadha_ui.urls')),

    # Medical registries
    path('AuShadha/icd10/', include('registry.icd10.urls')),
    path('AuShadha/icd10pcs/', include('registry.icd10pcs.urls')),
    path('AuShadha/drug_db/', include('registry.drug_db.urls')),
    path('AuShadha/fda_drug_db/', include('registry.drug_db.urls')),
    path('AuShadha/drugbankcadrugs/', include('registry.drug_db.drugbankca.urls')),

    # Future modules (commented out until migrated)
    # path('AuShadha/demographics/', include('demographics.demographics.urls')),
    # path('AuShadha/contact/', include('demographics.contact.urls')),
    # path('AuShadha/phone/', include('demographics.phone.urls')),
    # path('AuShadha/guardian/', include('demographics.guardian.urls')),
    # path('AuShadha/email_and_fax/', include('demographics.email_and_fax.urls')),
    #
    # path('AuShadha/family_history/', include('history.family_history.urls')),
    # path('AuShadha/social_history/', include('history.social_history.urls')),
    # path('AuShadha/medical_history/', include('history.medical_history.urls')),
    # path('AuShadha/surgical_history/', include('history.surgical_history.urls')),
    # path('AuShadha/obs_and_gyn/', include('history.obs_and_gyn.urls')),
    #
    # path('AuShadha/medication_list/', include('medication_list.urls')),
    # path('AuShadha/allergy_list/', include('allergy_list.urls')),
    # path('AuShadha/immunisation/', include('immunisation.urls')),
    #
    # path('AuShadha/visit/', include('visit.visit.urls')),
    # path('AuShadha/visit_complaints/', include('visit.visit_complaints.urls')),
    # path('AuShadha/visit_hpi/', include('visit.visit_hpi.urls')),
    # path('AuShadha/visit_ros/', include('visit.visit_ros.urls')),
    # path('AuShadha/visit_phyexam/', include('visit.visit_phyexam.urls')),
    # path('AuShadha/visit_assessment_and_plan/', include('visit.visit_assessment_and_plan.urls')),
    # path('AuShadha/visit_soap/', include('visit.visit_soap.urls')),
    # path('AuShadha/visit_prescription/', include('visit.visit_prescription.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve static files in development
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

# Run startup code (if needed)
try:
    from .startup import run
    run()
except Exception as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"Startup code failed: {e}")
