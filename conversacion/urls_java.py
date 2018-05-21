__author__ = 'brian'

from django.conf.urls import patterns, url
from conversacion import views_java as conversacion_java_views

urlpatterns = [
    url(r'^enviar_mensaje_protectora/$', conversacion_java_views.enviar_mensaje_protectora),
]
