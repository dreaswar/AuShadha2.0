from django.conf.urls import url

import AuShadha.settings

<<<<<<< HEAD
from django.contrib.auth import login, logout
=======
from django.contrib.auth import views as auth_views
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0

from .views import login_view, logout_view
from .models import AuShadhaUserForm


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [

  url(r'^login/$' ,login_view),
  url(r'^logout/$',logout_view),

#  url(r'^login/$' ,
<<<<<<< HEAD
#     login,
=======
#     auth_views.login,
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0
#     {'template_name':'registration/login.html',
#      'authentication_form': AuShadhaUserForm
#     },
#     name="login"
#  ),
<<<<<<< HEAD
  url(r'^logout/$',logout, name="logout"),
=======
  url(r'^logout/$',auth_views.logout, name="logout"),
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0

]
