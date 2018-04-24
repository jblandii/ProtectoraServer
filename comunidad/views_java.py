# -*- encoding: utf-8 -*-
import comunidad
from comunidad.models import ComunidadAutonoma

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
        token = datos.get('tokenFingido')

        if token == "JAMAGELEjamagele":
            comunidades = ComunidadAutonoma.objects.order_by("comunidad_autonoma")
            lista_comunidades = []
            for comunidad in comunidades:
                lista_comunidades.append({"pk": comunidad.pk,
                                          "comunidad_autonoma": comunidad.comunidad_autonoma})

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
    print "Comunidades"
    try:
        datos = json.loads(request.POST['data'])
        token = datos.get('tokenFingido')
        comunidad = datos.get('comunidad_autonoma')

        comunidad_autonoma = ComunidadAutonoma.objects.filter(comunidad_autonoma=comunidad)
        if comunidad_autonoma is not None:

            if token == "JAMAGELEjamagele":
                comunidades = ComunidadAutonoma.objects.order_by("comunidad_autonoma")

                lista_provincias = []
                for provincia in comunidades:
                    lista_provincias.append({"pk": provincia.pk,
                                             "provincia": provincia.provincia})

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
