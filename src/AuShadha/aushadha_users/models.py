##########################################################################
# Project: AuShadha Project User Models to customise Django User Model
#           and enable role and permission sharing
# License: GNU-GPL Version 3
# Author : Dr.Easwar T.R
# Date   : 03-09-2012
##########################################################################

"""
 Defining the models for AuShadha users

 This is a custom class to bind a logged in user to a Clinic and a Role

 All AuShadha uses should therefore be logged in and should have a role

 Fine grained permissions throughout the application can be set on role and
   permissions defined here

"""

from __future__ import absolute_import
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.base_user import AbstractBaseUser 
from django.db.models.signals import post_save
from django.dispatch import receiver 


AUSHADHA_USER_ROLES = (('audhadha_admin', 'AuShadha Admin'),
                       ('aushadha_user', 'AuShadha User'),
                       ('aushadha_staff', 'AuShadha Staff '),
                       ('aushadha_developer', 'AuShadha Developer'),
                       )



class AuShadhaUser(models.Model):

    """

     Defines AuShadhaUser class
     This is a model inheriting from User class that defines who uses AuShadha
     The user can have many roles pertaining to usage of the software.
     This is NOT the permission on the Clinic / the Patient.
     This is for managing / using AuShadha

    """
    aushadha_user_role = models.CharField("AuShadha User Role",
                          help_text=""" Users Role in AuShadha Software.
                               This is different from the role in the Clinic
                               """,
                          max_length=30,
                          choices=AUSHADHA_USER_ROLES,
                          default="aushadha_user"
                          )
    user = models.OneToOneField(User,on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_profile(sender,instance, created, **kwargs):
    if created:
        AuShadhaUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


    
class AuShadhaUserForm(AuthenticationForm):

    """
      Defines ModelForm for AuShadhaUser
      Generates the ModelForm for Login and authentication
    """
    
    def confirm_login_allowed(self, user):
        if not user.is_active or not user.is_validated:
            raise forms.ValidationError(
                'There was a problem with your login.', 
                code='invalid_login')

    model = AuShadhaUser
