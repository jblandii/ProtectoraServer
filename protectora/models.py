# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from comunidad.models import Provincia


class Protectora(models.Model):
    nombre = models.CharField(max_length=50)
    admin = models.ForeignKey(User)
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
    ANIMALES = (('Perro', 'Perro'),
                ('Gato', 'Gato'))
    mascota = models.CharField(max_length=10, choices=ANIMALES)
    raza = models.CharField(max_length=30)
    COLORES = (('Blanco', 'Blanco'),
               ('Negro', 'Negro'),
               ('Gris', 'Gris'),
               ('Marron', 'Marrón'))
    color = models.CharField(max_length=50, choices=COLORES)
    edad = models.IntegerField(default=0)
    PELAJES = (('Corto', 'Corto'),
               ('Largo', 'Largo'))
    tipo_pelaje = models.CharField(max_length=20, choices=PELAJES)
    SEXO = (('Macho', 'Macho'),
            ('Hembra', 'Hembra'))
    sexo = models.CharField(max_length=10, choices=SEXO)
    ESTADOS = (('Adopcion', 'Adopción'),
               ('Acogida', 'Acogida'))
    estado = models.CharField(max_length=15, choices=ESTADOS)
    TAMANIOS = (('Pequeno', 'Pequeño'),
                ('Mediano', 'Mediano'),
                ('Grande', 'Grande'))
    tamano = models.CharField(max_length=50, choices=TAMANIOS)
    peso = models.FloatField(default=0)
    enfermedad = models.CharField(max_length=255)
    vacuna = models.CharField(max_length=50)
    SINO = (('Si', 'Sí'),
            ('No', 'No'))
    chip = models.CharField(max_length=2, choices=SINO)
    fecha = models.DateField(auto_now_add=True)
    protectora = models.ForeignKey(Protectora)

    def __unicode__(self):
        return self.raza


class MeGusta(models.Model):
    animal = models.ForeignKey(Animal)
    usuario = models.ForeignKey(User)

    def __unicode__(self):
        return self.usuario


class Adopcion(models.Model):
    animal = models.ForeignKey(Animal)
    usuario = models.ForeignKey(User)
    fecha = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.fecha


class ImagenAnimal(models.Model):
    animal = models.ForeignKey(Animal)
    imagen = models.ImageField(upload_to="imagenes/animales")

    def __unicode__(self):
        return str(self.animal.pk)
