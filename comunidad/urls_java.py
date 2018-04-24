__author__ = 'JBlanDii'

from django.conf.urls import patterns, url
from comunidad import views_java as comunidad_java_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^comunidades/$', comunidad_java_views.comunidades),
    url(r'^provincias/$', comunidad_java_views.comunidades),
]
