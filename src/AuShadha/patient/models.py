################################################################################
# PROJECT      : AuShadha2.0
# Description  : Patient Models for managing patient
# Author       : Dr. Easwar T R
# Date         : 04-12-2016
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################


from __future__ import absolute_import
from __future__ import print_function
from django.db import models
from django.contrib.auth.models import User
import six

# AuShadha Imports
from aushadha_users.models import AuShadhaUser
from aushadha_base_models.models import AuShadhaBaseModel, \
                                        AuShadhaBaseModelForm
from clinic.models import Clinic


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
      for item in self._meta.get_fields_with_model():
        if item[0].__class__.__name__ not in ['OneToOneField']:
          exportable_fields[item[0][0].name] = item[0][0].value_from_object(self)
        else:
          continue
      return exportable_fields


    def __unicode__(self):
        if self.middle_name and self.last_name:
            return "%s %s %s" % (self.first_name.capitalize(),
                                 self.middle_name.capitalize(),
                                 self.last_name.capitalize()
                                 )
        elif self.last_name or self.middle_name:
          if self.last_name:
            return "%s %s" % (self.first_name.capitalize(),
                               self.last_name.capitalize())
          else:
            return "%s %s" % (self.first_name.capitalize(),
                              self.middle_name.capitalize())


    def check_before_you_add(self):
      """
        Checks whether the patient has already been registered in the
        database before adding.
      """
      all_pat = PatientDetail.objects.all()
      hosp_id = self.patient_hospital_id
      id_list = []
      if all_pat:
        for p in all_pat:
            id_list.append(p.patient_hospital_id)
        if hosp_id in id_list:
            error = "Patient is already registered"
            print(error)
            return False
        else:
            return True
      else:
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
        self.field_list = []
        print(self._meta.fields)
        for field in self._meta.fields:
            self.field_list.append(field)
        return self.field_list

    def _formatted_obj_data(self):
        if not self.field_list:
            _field_list()
        str_obj = "<ul>"
        for obj in self._field_list:
            _str += "<li>" + obj + "<li>"
            str_obj += _str
        str_obj += "</ul>"
        return str_obj


    def _set_full_name(self):

        """
            Defines and sets the Full Name for a Model on save.
            This stores the value under the self.full_name attribute.
            This is mainly intented for name display and search
        """

        if self.middle_name and self.last_name:
            self.full_name = six.text_type(self.first_name.capitalize() + " " +
                                     self.middle_name.capitalize() + " " +
                                     self.last_name.capitalize()
                                     )
        else:
          if self.last_name:
            self.full_name = six.text_type(self.first_name.capitalize() + " " +
                                     self.last_name.capitalize()
                                     )
          if self.middle_name:
            self.full_name = six.text_type(self.first_name.capitalize() + " " +
                                     self.middle_name.capitalize()
                                     )
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

    class Meta:
        model = PatientDetail
        exclude = ['parent_clinic',]
