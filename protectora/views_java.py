# -*- encoding: utf-8 -*-
import protectora
from comunidad.models import Provincia
from protectora.models import Animal, Protectora
from usuarios.models import Tokenregister

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
            # try:
            #     mascota = datos.get('mascota')
            #     # Filtro por perro o gato
            #     animales = animales.filter(mascota=mascota)
            # except:
            #     pass
            #
            # try:
            #     provincia = datos.get('provincia')
            #
            #     # Obtengo el objeto provincia filtrando por la provincia en la que vive el usuario.
            #     objeto_provincia = get_object_or_None(Provincia, provincia=provincia)
            #
            #     animales = animales.filter(provincia=objeto_provincia)
            # except:
            #     pass
            #
            # try:
            #     raza = datos.get('raza')
            #     animales = animales.filter(raza=raza)
            # except:
            #     pass
            #
            # try:
            #     color = datos.get('color')
            #     animales = animales.filter(color=color)
            # except:
            #     pass
            #
            # try:
            #     try:
            #         edad = datos.get('edad_menos')
            #         edad = animales.filter(edad__lte=edad)
            #     except:
            #         pass
            #
            #     try:
            #         edad = datos.get('edad_mas')
            #         edad = animales.filter(edad__gte=edad)
            #     except:
            #         pass
            # except:
            #     pass
            #
            # try:
            #     tipo_pelaje = datos.get('pelaje')
            #     tipo_pelaje = animales.filter(tipo_pelaje=tipo_pelaje)
            # except:
            #     pass
            #
            # try:
            #     sexo = datos.get('sexo')
            #     sexo = animales.filter(sexo=sexo)
            # except:
            #     pass
            #
            # try:
            #     estado = datos.get('estado')
            #     estado = animales.filter(estado=estado)
            # except:
            #     pass
            #
            # try:
            #     tamano = datos.get('tamano')
            #     tamano = animales.filter(tamano=tamano)
            # except:
            #     pass
            #
            # try:
            #     vacuna = datos.get('vacuna')
            #     vacuna = animales.filter(vacuna=vacuna)
            # except:
            #     pass
            #
            # try:
            #     chip = datos.get('chip')
            #     chip = animales.filter(chip=chip)
            # except:
            #     pass
            #
            # try:
            #     protectora = datos.get('protectora')
            #     protectora = animales.filter(protectora=protectora)
            # except:
            #     pass

            lista_animales = []
            for animal in animales:
                fotos = []
                for foto in animal.imagenanimal_set.all():
                    fotos.append({"foto": str(foto.imagen)})

                lista_animales.append({"pk": animal.pk,
                                       "nombre": animal.nombre,
                                       "raza": animal.raza.pk,
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
                                       "id_protectora": animal.protectora.pk})
                # "imagenes": fotos})

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
            print token
            protectoras = Protectora.objects.all()
            try:
                provincia = datos.get('provincia')

                # Obtengo el objeto provincia filtrando por la provincia en la que vive el usuario.
                objeto_provincia = get_object_or_None(Provincia, provincia=provincia)

                animales = protectoras.filter(provincia=objeto_provincia)
            except:
                pass

            lista_protectoras = []
            for protectora in protectoras:
                lista_protectoras.append({"pk": protectora.pk,
                                          "animal": protectora.provincia})

            if len(lista_protectoras) == 0:
                response_data = {'result': 'ok_sin_protectoras',
                                 'message': 'no hay protectoras con dichos filtros'}
            else:
                response_data = {'result': 'ok',
                                 'message': 'listado de animales',
                                 "lista_protectoras": lista_protectoras}
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
