############################################
#
#
#
#
#
############################################

from __future__ import absolute_import
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.base_user import AbstractBaseUser 
from django.db.models.signals import post_save
from django.dispatch import receiver 

from .models import AuShadhaUser

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class AuShadhaUserForm(ModelForm):
    class Meta: 
        model = AuShadhUser
        fields = ('aushadha_user_role')
                
