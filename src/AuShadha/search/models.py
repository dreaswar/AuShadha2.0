<<<<<<< HEAD
#################################################################################
# Project     : AuShadha2.0
# Description : Models for Search App for AuShadha
# Author      : Dr.Easwar T.R (see credits)
# License     : GNU-GPL Version 3 , see docs/LICENSE.txt
# Date        : 13-09-2018
################################################################################

"""

 Models to handle the Search Functions inside AuShadha

"""

from __future__ import absolute_import
from django.db import models
from django.contrib.auth.models import User

# AuShadha Imports
from aushadha_users.models import AuShadhaUser
from aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm


SEARCH_CHOICES = (
    ('patient', "Patient"),
    ('admission', "Admission"),
    ('visit', "Visit"),
    ('phone_number', "Phone Number"),
    ('address', "Address"),
    ('city', "City")
    )


class Search(AuShadhaBaseModel):

    """
     Basic Search Model 
    """

    def __init__(self, *args, **kwargs):
      super(Search,self).__init__(*args, **kwargs)
      self.__model_label__ = 'search'
      self._parent_model = 'clinic'


    search_for = models.CharField(max_length=200, default='patient', choices = SEARCH_CHOICES)

    def __unicode__(self):
        return '%s' % self.search_for
=======
from __future__ import absolute_import
from django.db import models

# Create your models here.
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0
