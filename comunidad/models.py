from __future__ import unicode_literals

from django.db import models


# Create your models here.
class ComunidadAutonoma(models.Model):
    comunidad_autonoma = models.CharField(max_length=25)

    def __unicode__(self):
        return self.comunidad_autonoma


# Create your models here.
class Provincia(models.Model):
    comunidad_autonoma = models.ForeignKey(ComunidadAutonoma)
    provincia = models.CharField(max_length=25)

    def __unicode__(self):
        return self.provincia
