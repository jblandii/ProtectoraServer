# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User

import comunidad
from comunidad.models import ComunidadAutonoma, Provincia

__author__ = 'brian'

import django.contrib.auth as auth
import django.http as http
from annoying.functions import get_object_or_None
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json


@csrf_exempt
def comunidades(request):
    print "Comunidades"
    try:
        datos = json.loads(request.POST['data'])
        tokenFingido = datos.get('tokenFingido')
        usuario_id = datos.get('usuario_id')

        if tokenFingido == "JAMAGELEjamagele":
            comunidades = ComunidadAutonoma.objects.order_by("comunidad_autonoma")
            lista_comunidades = []
            for comunidad in comunidades:
                lista_comunidades.append({"pk": comunidad.pk,
                                          "comunidad_autonoma": comunidad.comunidad_autonoma})
            if usuario_id is not None:
                usuario = get_object_or_None(User, pk=usuario_id)
                comunidad = usuario.datosextrauser.provincia.comunidad_autonoma.pk
                response_data = {
                    'result': 'ok',
                    'message': "listado comunidades",
                    'comunidades': lista_comunidades,
                    'comunidad_usuario': comunidad
                }
            else:
                response_data = {
                    'result': 'ok',
                    'message': "listado comunidades",
                    'comunidades': lista_comunidades
                }
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data = {
                'result': 'error',
                'message': "error de token"
            }
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0002', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def provincias(request):
    print "Provincias"
    try:
        datos = json.loads(request.POST['data'])
        token = datos.get('tokenFingido')
        id_comunidad = datos.get('id_comunidad')
        usuario_id = datos.get('usuario_id')

        provincias = Provincia.objects.filter(comunidad_autonoma=id_comunidad).order_by("provincia")
        if provincias is not None:

            if token == "JAMAGELEjamagele":

                lista_provincias = []
                for provincia in provincias:
                    lista_provincias.append({"pk": provincia.pk,
                                             "provincia": provincia.provincia})

                if usuario_id is not None:
                    usuario = get_object_or_None(User, pk=usuario_id)
                    provincia = usuario.datosextrauser.provincia
                    response_data = {
                        'result': 'ok',
                        'message': "listado provincias",
                        'provincias': lista_provincias,
                        'provincia_usuario': provincia.pk
                    }
                else:
                    response_data = {
                        'result': 'ok',
                        'message': "listado provincias",
                        'provincias': lista_provincias
                    }
                return http.HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                response_data = {
                    'result': 'error',
                    'message': "error de token"
                }
                return http.HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data = {
                'result': 'error',
                'message': "no se recibe provincia"
            }
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")


    except Exception as e:
        response_data = {'errorcode': 'U0002', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")
