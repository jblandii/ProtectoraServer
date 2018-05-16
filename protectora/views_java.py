# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User

from comunidad.models import Provincia
from protectora.models import Animal, Protectora, MeGusta
from usuarios.views_java import comprobar_usuario

__author__ = 'brian'

import django.contrib.auth as auth
import django.http as http
from annoying.functions import get_object_or_None
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json


@csrf_exempt
def cargar_animales(request):
    print "carga de animales"
    try:
        datos = json.loads(request.POST['data'])

        try:
            token = datos.get('token')
            usuario_id = datos.get('usuario_id')
            animales = Animal.objects.all()
            usuario = get_object_or_None(User, pk=usuario_id)
            try:
                mascota = datos.get('mascota')
                if mascota:
                    animales = animales.filter(mascota=mascota)
            except:
                pass

            try:
                provincia = datos.get('provincia')
                if provincia:
                    # Obtengo el objeto provincia filtrando por la provincia en la que vive el usuario.
                    objeto_provincia = get_object_or_None(Provincia, provincia=provincia)

                animales = animales.filter(provincia=objeto_provincia)
            except:
                pass

            try:
                raza = datos.get('raza')
                if raza:
                    animales = animales.filter(raza=raza)
            except:
                pass

            try:
                color = datos.get('color')
                if color:
                    animales = animales.filter(color=color)
            except:
                pass

            try:
                try:
                    edadmenos = datos.get('edad_menos')
                    if edadmenos:
                        edad = animales.filter(edad__lte=edadmenos)
                except:
                    pass

                try:
                    edadmas = datos.get('edad_mas')
                    if edadmas:
                        edad = animales.filter(edad__gte=edadmas)
                except:
                    pass
            except:
                pass

            try:
                tipo_pelaje = datos.get('pelaje')
                if tipo_pelaje:
                    tipo_pelaje = animales.filter(tipo_pelaje=tipo_pelaje)
            except:
                pass

            try:
                sexo = datos.get('sexo')
                if sexo:
                    sexo = animales.filter(sexo=sexo)
            except:
                pass

            try:
                estado = datos.get('estado')
                if estado:
                    estado = animales.filter(estado=estado)
            except:
                pass

            try:
                tamano = datos.get('tamano')
                if tamano:
                    tamano = animales.filter(tamano=tamano)
            except:
                pass

            try:
                vacuna = datos.get('vacuna')
                if vacuna:
                    vacuna = animales.filter(vacuna=vacuna)
            except:
                pass

            try:
                chip = datos.get('chip')
                if chip:
                    chip = animales.filter(chip=chip)
            except:
                pass

            try:
                protectora = datos.get('protectora')
                if protectora:
                    protectora = animales.filter(protectora=protectora)
            except:
                pass

            lista_animales = []
            for animal in animales:
                fotos = []
                for foto in animal.imagenanimal_set.all():
                    # fotos.append({"foto": str(foto.imagen)})
                    fotos.append(str(foto.imagen))

                meGusta = False

                animales = MeGusta.objects.filter(animal=animal)
                if animales.count() > 0:
                    animales = animales.filter(usuario=usuario)
                    if animales.count() > 0:
                        meGusta = True

                lista_animales.append({"pk": animal.pk,
                                       "nombre": animal.nombre,
                                       "raza": animal.raza.nombre,
                                       "mascota": animal.mascota,
                                       "color": animal.color,
                                       "edad": animal.edad,
                                       "pelaje": animal.tipo_pelaje,
                                       "sexo": animal.sexo,
                                       "tamano": animal.tamano,
                                       "peso": animal.peso,
                                       "enfermedad": animal.enfermedad,
                                       "vacuna": animal.vacuna,
                                       "chip": animal.chip,
                                       "estado": animal.estado,
                                       "id_protectora": animal.protectora.pk,
                                       "foto": fotos[0],
                                       "me_gusta": meGusta})

                if len(lista_animales) == 0:
                    response_data = {'result': 'ok_sin_animales',
                                     'message': 'no hay animales con dichos filtros'}
                else:
                    response_data = {'result': 'ok',
                                     'message': 'listado de animales',
                                     "lista_animales": lista_animales}
        except:
            response_data = {'result': 'error', 'message': 'error de token o usuario'}

        # if token is not None:
        #
        #     # Obtengo el objeto provincia filtrando por la provincia en la que vive el usuario.
        #     objeto_provincia = get_object_or_None(Provincia, provincia=provincia)
        #
        #     animales = Animal.objects.filter(protectora__provincia=objeto_provincia)
        #
        #     print animales.count()
        #
        #     lista_animales = []
        #
        #     response_data = {'result': 'ok', 'message': 'usuario existente'}
        # else:
        #     response_data = {'result': 'ok', 'message': 'usuario existente'}

        # user = get_object_or_None(Tokenregister, token=token)
        # usu = user.user.datosextrauser.provincia
        print response_data
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0002', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def cargar_protectoras(request):
    print "carga de protectoras"
    try:
        datos = json.loads(request.POST['data'])

        try:
            token = datos.get('token')
            usuario_id = datos.get('usuario_id')
            protectoras = Protectora.objects.all()

            lista_protectoras = []
            for protectora in protectoras:
                lista_protectoras.append({
                    "pk": protectora.pk,
                    "nombre": protectora.nombre,
                    "direccion": protectora.direccion,
                    "codigo_postal": protectora.cod_postal,
                    "provincia": protectora.provincia.provincia})

            if len(lista_protectoras) == 0:
                response_data = {'result': 'ok_sin_protectoras',
                                 'message': 'no hay animales con dichos filtros'}
            else:
                response_data = {'result': 'ok',
                                 'message': 'listado de protectoras',
                                 "lista_protectoras": lista_protectoras}
            print response_data
        except:
            response_data = {'result': 'error', 'message': 'error de token o usuario'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0002', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def cargar_animales_me_gusta(request):
    print "carga de animales que gustan"
    try:
        datos = json.loads(request.POST['data'])

        try:
            token = datos.get('token')
            usuario_id = datos.get('usuario_id')
            if comprobar_usuario(datos):
                usuario = get_object_or_None(User, pk=usuario_id)
                animales = MeGusta.objects.filter(usuario=usuario)
                lista_animales = []
                lista_mg = []
                for mg in animales:
                    lista_mg.append(mg.animal)

                for animal in lista_mg:
                    fotos = []
                    for foto in animal.imagenanimal_set.all():
                        fotos.append(str(foto.imagen))

                    meGusta = False

                    animales = MeGusta.objects.filter(animal=animal)
                    if animales.count() > 0:
                        animales = animales.filter(usuario=usuario)
                        if animales.count() > 0:
                            meGusta = True

                    lista_animales.append({"pk": animal.pk,
                                           "nombre": animal.nombre,
                                           "raza": animal.raza.nombre,
                                           "mascota": animal.mascota,
                                           "color": animal.color,
                                           "edad": animal.edad,
                                           "pelaje": animal.tipo_pelaje,
                                           "sexo": animal.sexo,
                                           "tamano": animal.tamano,
                                           "peso": animal.peso,
                                           "enfermedad": animal.enfermedad,
                                           "vacuna": animal.vacuna,
                                           "chip": animal.chip,
                                           "estado": animal.estado,
                                           "id_protectora": animal.protectora.pk,
                                           "foto": fotos[0],
                                           "me_gusta": meGusta})

                    if len(lista_animales) == 0:
                        response_data = {'result': 'ok_sin_animales',
                                         'message': 'no hay animales con dichos filtros'}
                    else:
                        response_data = {'result': 'ok',
                                         'message': 'listado de animales',
                                         "lista_animales": lista_animales}
            else:
                response_data = {'result': 'error', 'message': 'error de token o usuario'}
        except:
            response_data = {'result': 'error', 'message': 'error de token o usuario'}

        print response_data
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0002', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def dar_mg(request):
    print "dar/quitar mg"
    try:
        datos = json.loads(request.POST['data'])

        try:
            usuario_id = datos.get('usuario_id')
            token = datos.get('token')
            animal_id = datos.get('animal')
            megusta = datos.get('me_gusta')
            print usuario_id
            print token
            if comprobar_usuario(datos):
                usuario = get_object_or_None(User, pk=usuario_id)
                animal = get_object_or_None(Animal, pk=animal_id)
                if animal is not None:
                    if megusta == "true":
                        mg = MeGusta.objects.filter(usuario=usuario)
                        if mg is not None:
                            mg = mg.filter(animal=animal)
                            if mg is not None:
                                mg.delete()
                                response_data = {'result': 'ok',
                                                 'message': 'Se ha quitado mg correctamente'}

                    else:
                        mg = MeGusta.objects.create(animal=animal, usuario=usuario)
                        mg.save()
                        response_data = {'result': 'ok',
                                         'message': 'Se ha dado mg correctamente'}
                else:
                    response_data = {'result': 'ok',
                                     'message': 'no hay animal'}
            else:
                response_data = {'result': 'error', 'message': 'error de token o usuario'}
        except:
            response_data = {'result': 'error', 'message': 'error de token o usuario'}

        print response_data
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0002', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")
