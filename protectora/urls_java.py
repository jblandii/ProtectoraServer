# -*- encoding: utf-8 -*-

__author__ = 'brian'

from django.conf.urls import patterns, url
from protectora import views_java as protectora_java_views

urlpatterns = [
    url(r'^cargar_animales/$', protectora_java_views.cargar_animales),
    url(r'^cargar_protectoras/$', protectora_java_views.cargar_protectoras),
]
