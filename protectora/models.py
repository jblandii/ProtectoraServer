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
    descripcion = models.CharField(max_length=500, blank=True, null=True)

    def __unicode__(self):
        return self.nombre


class RazaAnimal(models.Model):
    nombre = models.CharField(max_length=30)

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
        return self.protectora.nombre


class Animal(models.Model):
    ANIMALES = (('Perro', 'Perro'),
                ('Gato', 'Gato'))
    nombre = models.CharField(max_length=15)
    mascota = models.CharField(max_length=10, choices=ANIMALES)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    raza = models.ForeignKey(RazaAnimal)
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
        return self.nombre


class MeGusta(models.Model):
    animal = models.ForeignKey(Animal)
    usuario = models.ForeignKey(User)

    def __unicode__(self):
        return self.usuario.username


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
        return str(self.animal.nombre)


class ImagenProtectora(models.Model):
    protectora = models.ForeignKey(Protectora)
    imagen = models.ImageField(upload_to="imagenes/protectora")

    def __unicode__(self):
        return self.protectora.nombre
