from django.db import models
import datetime
from django.forms import ModelForm
from django.db.models.signals import post_save

import os

PROJECT_PATH = os.path.dirname("__file__")

# class Cliente(models.Model):
#     nombre = models.CharField(max_length=80)
#     foto = models.FileField()
#
#     def __unicode__(self):
#         return u"%s" % self.nombre
#
#
# class Trabajo(models.Model):
#     cliente = models.ForeignKey(Cliente)
#     nombre = models.CharField(max_length=150)
#     fecha = models.DateField(auto_now=True)
#     plataformas = models.CharField(max_length=150)
#     enlace = models.CharField(max_length=200)
#     descripcion = models.CharField(max_length=150)
#
#     def __unicode__(self):
#         return u"%s" % self.nombre