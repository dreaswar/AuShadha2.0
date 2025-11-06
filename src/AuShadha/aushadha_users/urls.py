from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view, logout_view
from .models import AuShadhaUserForm

# Admin autodiscover is no longer needed in Django 4.2
from django.contrib import admin

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
