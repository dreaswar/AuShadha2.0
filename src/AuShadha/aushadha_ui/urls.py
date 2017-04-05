"""AuShadha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import absolute_import
from django.conf.urls import url , include
from django.contrib import admin

from aushadha_ui.views import home
import AuShadha.settings

from .views import home,get_reference_apps, installed_apps
from .dijit_widgets.pane import render_aushadha_ui_pane
#from data.views import installed_apps

urlpatterns = [
    #url(r'', home ),
    
    url(r'^$',  home, name='home'),
    
    url(r'json/installed_apps/$',  
         installed_apps, 
         name='installed_apps'),
    
    url(r'render/pane/$',  
         render_aushadha_ui_pane, 
         name='render_aushadha_ui_pane'),
    
    url(r'get/reference_apps/$',  
          get_reference_apps, 
          name='get_reference_apps'),

    #(r'^AuShadha/json_data/', include('json_data.urls') ),
    #(r'^AuShadha/widgets/', include('widgets.urls') ),

]