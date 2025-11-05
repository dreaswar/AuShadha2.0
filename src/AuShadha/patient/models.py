################################################################################
# PROJECT      : AuShadha2.0
# Description  : Patient Models for managing patient
# Author       : Dr. Easwar T R
# Date         : 04-12-2016
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################


import logging
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

# AuShadha Imports
from aushadha_users.models import AuShadhaUser
from aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm
from clinic.models import Clinic

from .dijit_fields_constants import PATIENT_DETAIL_FORM_CONSTANTS

# Initialize logger
logger = logging.getLogger(__name__)

# Get APP_ROOT_URL from settings
APP_ROOT_URL = getattr(settings, 'APP_ROOT_URL', '/AuShadha/')

DEFAULT_PATIENT_DETAIL_FORM_EXCLUDES=('parent_clinic',)

class PatientDetail(AuShadhaBaseModel):

    """
      Patient Model definition for Registration, 
      Name entry and Hospital ID Generation
    """

   # Some data to Generate the URLS

    def __init__(self,*args,**kwargs):
      super(PatientDetail,self).__init__(*args, **kwargs)
      self.__model_label__ = "patient"
      self._parent_model = 'parent_clinic'


    # Model attributes
    patient_hospital_id = models.CharField('Hospital ID',
                                            max_length=15,
                                           unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30,
                                   help_text="Please enter Initials / Middle Name", blank=True,
                                   null=True)
    last_name = models.CharField(max_length=30,
                                 blank=True,
                                 null=True,
                                 help_text="Enter Initials / Last Name"
                                 )
    full_name = models.CharField(max_length=100,
                                 editable=False,
                                 null=False,
                                 blank=False
                                 )
    age = models.CharField(max_length=10, blank=True, null=True)
    sex = models.CharField(max_length=6,
                           choices=(("Male", "Male"),
                                    ("Female", "Female"),
                                    ("Others", "Others")
                                    ),
                           default = "Male")
    parent_clinic = models.ForeignKey(Clinic, on_delete = models.CASCADE )



    class Meta:
        verbose_name = "Patient - Basic Data"
        verbose_name_plural = "Patient - Basic Data"
        ordering = ('first_name',
                    'middle_name',
                    'last_name',
                    'age', 'sex',
                    'patient_hospital_id'
                    )
        unique_together = ('patient_hospital_id', 'parent_clinic')


    def get_all_json_exportable_fields(self):
        """
        Gets the JSON exportable fields and its values as key, value pair
        This skips AutoField, OneToOneField type of field
        """
        exportable_fields = {}
        for field in self._meta.get_fields():
            # Skip AutoField, OneToOneField, and related fields
            if not isinstance(field, (models.AutoField, models.OneToOneField)) and field.concrete:
                try:
                    exportable_fields[field.name] = field.value_from_object(self)
                except AttributeError:
                    logger.warning(f"Could not export field: {field.name}")
                    continue
        return exportable_fields


    def __str__(self):
        """String representation of patient (Python 3)"""
        if self.full_name:
            return self.full_name

        if self.middle_name and self.last_name:
            return f"{self.first_name.capitalize()} {self.middle_name.capitalize()} {self.last_name.capitalize()}"
        elif self.last_name:
            return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"
        elif self.middle_name:
            return f"{self.first_name.capitalize()} {self.middle_name.capitalize()}"
        return self.first_name.capitalize()


    def check_before_you_add(self):
        """
        Checks whether the patient has already been registered in the
        database before adding. Uses efficient database query.
        """
        if not self.patient_hospital_id:
            return True

        # Efficient query - only checks if hospital ID exists
        # Exclude self if this is an update (has pk)
        queryset = PatientDetail.objects.filter(
            patient_hospital_id=self.patient_hospital_id
        )
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        if queryset.exists():
            error_msg = f"Patient with hospital ID '{self.patient_hospital_id}' is already registered"
            logger.error(error_msg)
            raise ValidationError(error_msg)
        return True

    def save(self, *args, **kwargs):

        """
          Custom Save Method needs to be defined.
          This should check for:
          1. Whether the patient is registered before.
          2. Patient DOB / Age Verfication and attribute setting
          3. Setting the full_name attribute
        """

        self.check_before_you_add()
        self._set_full_name()
    #     self._set_age()
        super(PatientDetail, self).save(*args, **kwargs)


    def _field_list(self):
        """Get list of model fields"""
        self.field_list = []
        logger.debug(f"Fields for {self.__class__.__name__}: {self._meta.fields}")
        for field in self._meta.fields:
            self.field_list.append(field)
        return self.field_list

    def _formatted_obj_data(self):
        """
        Format object data as HTML list.
        Note: This method appears unused and has been fixed for completeness.
        Consider removing if not needed.
        """
        if not hasattr(self, 'field_list') or not self.field_list:
            self._field_list()

        str_obj = "<ul>"
        for field in self.field_list:
            str_obj += f"<li>{field.name}: {getattr(self, field.name, 'N/A')}</li>"
        str_obj += "</ul>"
        return str_obj


    def _set_full_name(self):
        """
        Defines and sets the Full Name for a Model on save.
        This stores the value under the self.full_name attribute.
        This is mainly intended for name display and search.
        """
        parts = [self.first_name.capitalize()]

        if self.middle_name:
            parts.append(self.middle_name.capitalize())
        if self.last_name:
            parts.append(self.last_name.capitalize())

        self.full_name = " ".join(parts)
        return self.full_name


    def _set_age(self):

        """ Check DOB and Age. See Which one to set.
            Dont set age if DOB is given.
            Dont allow age > 120 to be set.
            This should be called before Form & Model save.
            If this returns false, the save should fail raising proper Exception
        """

        if self.date_of_birth:
            min_allowed_dob = datetime.datetime(1900, 0o1, 0o1)
            max_allowed_dob = datetime.datetime.now()
            if self.date_of_birth >= min_allowed_dob and \
                self.date_of_birth <= max_allowed_dob:
                self.age = "%.2f" % (
                    round((max_allowed_dob - self.date_of_birth).days / 365.0, 2))
                return True
            else:
                raise Exception(
                    "Invalid Date: Date should be from January 01 1900 to Today's Date")
        else:
            if self.age and int(self.age[0:3]) <= 120:
                self.date_of_bith = None
                return True
            else:
                raise Exception("Invalid Date of Birth / Age Supplied")
                return False




class PatientDetailForm(AuShadhaBaseModelForm):

    """
        ModelForm for Patient Basic Data
    """

    __form_name__ = "Patient Detail Form"

    dijit_fields = PATIENT_DETAIL_FORM_CONSTANTS

    class Meta:
        model = PatientDetail
        exclude = DEFAULT_PATIENT_DETAIL_FORM_EXCLUDES

