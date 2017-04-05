from django.conf.urls import url

import AuShadha.settings

from django.contrib.auth import views as auth_views

from .views import login_view, logout_view
from .models import AuShadhaUserForm


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [

  url(r'^login/$' ,login_view),
  url(r'^logout/$',logout_view),

#  url(r'^login/$' ,
#     auth_views.login,
#     {'template_name':'registration/login.html',
#      'authentication_form': AuShadhaUserForm
#     },
#     name="login"
#  ),
  url(r'^logout/$',auth_views.logout, name="logout"),

]
