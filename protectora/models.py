# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User
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

# Create your models here.
class Protectora(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    provincia = models.ForeignKey(Provincia)
    cod_postal = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nombre

class RedSocial(models.Model):
    protectora = models.ForeignKey(Protectora)
    TIPOS = (('Facebook', 'Facebook'),
             ('Instagram', 'Instagram'),
             ('Twitter', 'Twitter'))
    tipo = models.CharField(max_length=15, choices=TIPOS)
    valor = models.CharField(max_length=512)

    def __unicode__(self):
        return self.tipo


class Animal(models.Model):
    raza = models.CharField(max_length=30)
    color = models.CharField(max_length=50)
    edad = models.IntegerField(default=0)
    PELAJES = (('Corto', 'Corto'),
               ('Largo', 'Largo'))
    tipo_pelaje = models.CharField(max_length=20, choices=PELAJES)
    SEXO = (('Macho', 'Macho'),
            ('Hembra', 'Hembra'))
    sexo = models.CharField(max_length=10, choices=SEXO)
    ESTADOS = (('Adopción', 'Adopción'),
               ('Acogida', 'Acogida'))
    estado = models.CharField(max_length=15, choices=ESTADOS)
    TAMANIOS = (('Pequeño', 'Pequeño'),
                ('Mediano', 'Mediano'),
                ('Grande', 'Grande'))
    tamano = models.CharField(max_length=50, choices=TAMANIOS)
    peso = models.FloatField(default=0)
    enfermedad = models.CharField(max_length=255)
    vacuna = models.CharField(max_length=50)
    SINO = (('Sí', 'Sí'),
            ('No', 'No'))
    chip = models.CharField(max_length=2, choices=SINO)
    protectora = models.ForeignKey(Protectora)

    def __unicode__(self):
        return self.raza


class Adopcion(models.Model):
    animal = models.ForeignKey(Animal)
    usuario = models.ForeignKey(User)
    fecha = models.DateField()

    def __unicode__(self):
        return self.fecha


class Foto(models.Model):
    animal = models.ForeignKey(Animal)
    foto = models.ImageField()

    def __unicode__(self):
        return str(self.animal.pk)
