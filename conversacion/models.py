from __future__ import unicode_literals

import user
import protectora

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Conversacion(models.Model):
    protectora = models.ForeignKey(User, related_name="admin")
    usuario = models.ForeignKey(User, related_name="user")

    def __unicode__(self):
        return self.protectora.username + " - " + self.usuario.username


class Mensaje(models.Model):
    usuario = models.ForeignKey(User)
    mensaje = models.CharField(max_length=512)
    hora = models.DateTimeField(auto_now_add=True)
    conversacion = models.ForeignKey(Conversacion)

    def __unicode__(self):
        return self.usuario.username
