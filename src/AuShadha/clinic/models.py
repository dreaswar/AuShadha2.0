#################################################################################
# Project     : AuShadha2.0
# Description : Models for Clinic, Departments and Staff
# Author      : Dr.Easwar T.R (see credits)
# License     : GNU-GPL Version 3 , see docs/LICENSE.txt
# Date        : 04-12-2016
################################################################################

"""

 Models to handle the Clinic, Address, Staff and Departments
 User permissions, roles are set here.
 Basic data about the Clinic is set here.

"""

from __future__ import absolute_import
from django.db import models
from django.contrib.auth.models import User

# AuShadha Imports
from aushadha_users.models import AuShadhaUser
from aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm


CLINIC_NATURE_CHOICES = (
    ("primary_health_centre", "Primary Health Centre"),
    ('community_health_centre', "Community Health Centre"),
    ("poly_clinic", "Poly Clinic"),
    ("speciality_clinic", "Speciality Clinic"),
    ('district_hospital', "District Hospital"),
    ('tertiary_referral_centre', "Tertiary Referral Centre")
)

CLINIC_STAFF_ROLE = (
    ("non_clinical_staff", "Non Clinical Staff"),
    ('secretary', 'Secretary'),
    ('clinic_admin', "Clinic Administrator"),
    ('clinical_staff', "Clinical Staff"),
    ('nurse', "Nurse"),
    ('physio', "Physiotherapist"),
    ("doctor", "Doctor"),
)

AUSHADHA_USER_ROLES = (('audhadha_admin', 'AuShadha Admin'),
                       ('aushadha_user', 'AuShadha User'),
                       ('aushadha_staff', 'AuShadha Staff '),
                       ('aushadha_developer', 'AuShadha Developer'),
                       )




class Clinic(AuShadhaBaseModel):

  """

   Model class for Clinic

   Defines the clinic

    -- name of clinic        --> Name

    -- nature_of_clinic      --> Whether its primary center / referral centre


  """

  def __init__(self, *args, **kwargs):

      super(Clinic,self).__init__(*args, **kwargs)
      self.__model_label__ = 'clinic'
      self._parent_model = 'clinic'

  name_of_clinic = models.CharField(max_length=200)
  nature_of_clinic = models.CharField(max_length=200, choices = CLINIC_NATURE_CHOICES)

  def __str__(self):
      return '%s (%s)' %(self.name_of_clinic, self.nature_of_clinic)


class Address(AuShadhaBaseModel):

    """
     Basic Contact attributes of the Clinic
    """

    def __init__(self, *args, **kwargs):

      super(Address,self).__init__(*args, **kwargs)
      self.__model_label__ = 'address'
      self._parent_model = 'clinic'


    building_no = models.CharField(max_length=200, default= 'Tamil Nadu')
    street_name = models.TextField()
    city_or_town = models.CharField(max_length=200, default= 'Coimbatore')
    district = models.CharField(max_length=200, default= 'Coimbatore')
    state = models.CharField(max_length=200, default= 'Tamil Nadu')
    country = models.CharField(max_length=200, default = 'India')
    postal_code = models.CharField("Postal Code", max_length=200)

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __unicode__(self):
        return '%s - %s, %s\n %s,%s, %s -%s' %(self.building_no,
                                            self.street_name,
                                            self.city_or_town,
                                            self.district,
                                            self.state,
                                            self.country,
                                            self.postal_code
                                            )



class Phone(AuShadhaBaseModel):

    """
     Basic Contact attributes of the Clinic
    """

    def __init__(self, *args, **kwargs):

      super(Phone,self).__init__(*args, **kwargs)
      self.__model_label__ = 'phone'
      self._parent_model = 'clinic'


    country_code    = models.PositiveIntegerField( default = 91)
    area_code    = models.PositiveIntegerField(default = 422)
    phone_number = models.PositiveIntegerField()

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)


    def __unicode__(self):
        return '%s-%s-%s' % (self.country_code, self.area_code,self.phone_number)


class Fax(AuShadhaBaseModel):

    """
     Basic Contact attributes of the Clinic
    """

    def __init__(self, *args, **kwargs):
      super(Fax,self).__init__(*args, **kwargs)
      self.__model_label__ = 'fax'
      self._parent_model = 'clinic'


    fax_number = models.CharField(max_length=200)

    clinic = models.ForeignKey(Clinic, on_delete = models.CASCADE)

    def __unicode__(self):
        return '%s' % self.fax_number

class Email(AuShadhaBaseModel):

    """
     Basic Contact attributes of the Clinic
    """

    def __init__(self, *args, **kwargs):

      super(Email,self).__init__(*args, **kwargs)
      self.__model_label__ = 'email'
      self._parent_model = 'clinic'


    email_address = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete = models.CASCADE )

    def __unicode__(self):
        return '%s' % self.email_address


class Website(AuShadhaBaseModel):

    """
     Basic Contact attributes of the Clinic
    """

    def __init__(self, *args, **kwargs):

      super(Website,self).__init__(*args, **kwargs)
      self.__model_label__ = 'website'
      self._parent_model = 'clinic'


    website_address = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete = models.CASCADE )

    def __unicode__(self):
        return '%s' % self.website_address


class Department(AuShadhaBaseModel):

    """
     Basic Contact attributes of the Clinic
    """

    def __init__(self, *args, **kwargs):
      super(Department,self).__init__(*args, **kwargs)
      self.__model_label__ = 'department'
      self._parent_model = 'clinic'


    name_of_department = models.CharField(max_length=100, unique=True)
    clinic = models.ForeignKey(Clinic, on_delete = models.CASCADE )

    def __unicode__(self):
        return "%s" % self.name_of_department


class Staff(AuShadhaBaseModel):

    """
     Basic Contact attributes of the Clinic
    """

    def __init__(self, *args, **kwargs):
      super(Staff,self).__init__(*args, **kwargs)
      self.__model_label__ = 'staff'
      self._parent_model = 'department'


#    staff_detail  = models.ForeignKey(AuShadhaUser)
    clinic_staff_role = models.CharField("Staff Role",max_length=100,
                                         help_text=" This is the Role of the Staff in the Clinic",
                                         choices=CLINIC_STAFF_ROLE)
    aushadha_user_role = models.CharField("AuShadha User Role",
                                          help_text=""" Users Role in AuShadha Software.
                                                           This is different from the role in the Clinic""",
                                          max_length=30,
                                          choices=AUSHADHA_USER_ROLES,
                                          default="aushadha_user"
                                          )
    user = models.OneToOneField(User, on_delete = models.CASCADE )
    is_staff_hod = models.BooleanField("Is Staff Head of the Department",default=None)
    department    = models.ForeignKey(Department, on_delete = models.CASCADE )

    def __unicode__(self):
        return "%s" % self.user.username

    def is_staff_provider(self):
        staff_obj = self
        staff_role = self.clinic_staff_role
        if staff_role == 'doctor':
            return True
        else:
            return False

