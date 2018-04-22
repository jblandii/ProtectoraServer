# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from configuracion import views as configuracion_views
from django.contrib.auth.decorators import login_required
import views

from django.contrib import admin

admin.autodiscover()

urlpatterns = [

    # url(r'^tienda/$', views.Tienda.as_view(), name='tienda'),

]
