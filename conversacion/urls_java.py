__author__ = 'brian'

from django.conf.urls import patterns, url
from conversacion import views_java as conversacion_java_views

urlpatterns = [
    url(r'^enviar_mensaje_protectora/$', conversacion_java_views.enviar_mensaje_protectora),
    url(r'^cargar_conversaciones/$', conversacion_java_views.cargar_conversaciones),
    url(r'^cargar_mensajes/$', conversacion_java_views.cargar_mensajes),
]
