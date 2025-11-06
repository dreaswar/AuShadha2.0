from django.urls import re_path

import AuShadha.settings
from django.contrib.auth import login, logout
from .views import login_view, logout_view
from .models import AuShadhaUserForm


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [

  re_path(r'^login/$', login_view, {'template_name': 'registration/login_modern.html'}),
  re_path(r'^logout/$',logout_view),

#  re_path(r'^login/$' ,
#     login,
#     {'template_name':'registration/login.html',
#      'authentication_form': AuShadhaUserForm
#     },
#     name="login"
#  ),
  re_path(r'^logout/$',logout, name="logout"),

]
