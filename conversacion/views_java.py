import django.http as http
from annoying.functions import get_object_or_None
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

from conversacion.models import Conversacion, Mensaje
from protectora.models import Protectora
from usuarios.views_java import comprobar_usuario


@csrf_exempt
def enviar_mensaje_protectora(request):
    print "enviando mensaje a la protectora"
    try:
        datos = json.loads(request.POST['data'])
        try:
            if comprobar_usuario(datos):
                protectora_id = datos.get('protectora')
                usuario_id = datos.get('usuario_id')
                mensaje = datos.get('message')
                print mensaje
                try:
                    protectora_objeto = get_object_or_None(Protectora, pk=protectora_id)
                    usuario_objeto = get_object_or_None(User, pk=usuario_id)
                except:
                    response_data = {'result': 'error', 'message': 'Protectora o Usuario no encontrados'}
                    return http.HttpResponse(json.dumps(response_data), content_type="application/json")

                admin_protectora = protectora_objeto.admin.pk

                usuario_objeto2 = get_object_or_None(User, pk=admin_protectora)

                conversacion = get_object_or_None(Conversacion, protectora=usuario_objeto2, usuario=usuario_objeto)
                print conversacion

                if conversacion is None:
                    conversacion = Conversacion.objects.create(protectora=usuario_objeto2,
                                                               usuario=usuario_objeto)
                    conversacion.save()
                    print conversacion
                else:
                    conversacion = get_object_or_None(Conversacion,
                                                      protectora=usuario_objeto2,
                                                      usuario=usuario_objeto)
                    print conversacion

                mensaje = Mensaje.objects.create(usuario=usuario_objeto, mensaje=mensaje, conversacion=conversacion)
                mensaje.save()

                response_data = {'result': 'ok',
                                 'message': 'mensaje enviado'}
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
def cargar_conversaciones(request):
    print "carga de conversaciones"
    try:
        datos = json.loads(request.POST['data'])

        try:
            if comprobar_usuario(datos):
                usuario_id = datos.get("usuario_id")
                usuario = get_object_or_None(User, pk=usuario_id)
                conversaciones = Conversacion.objects.filter(usuario=usuario).order_by('-pk')

                lista_conversaciones = []
                for conversacion in conversaciones:
                    protectora = conversacion.protectora.protectora_set.all()
                    protectora_objeto = get_object_or_None(Protectora, pk=protectora)
                    print protectora_objeto

                    lista_conversaciones.append({
                        'pk': str(conversacion.pk),
                        'protectora': {
                            "pk": protectora_objeto.pk,
                            "nombre": protectora_objeto.nombre,
                            "direccion": protectora_objeto.direccion,
                            "codigo_postal": protectora_objeto.cod_postal,
                            "provincia": protectora_objeto.provincia.provincia,
                            "descripcion": protectora_objeto.descripcion
                        }
                    })

                response_data = {'result': 'ok',
                                 'message': 'listado de conversaciones',
                                 "lista_conversaciones": lista_conversaciones}
            else:
                response_data = {'result': 'error', 'message': 'error de token o usuario'}
        except:
            response_data = {'result': 'error', 'message': 'error de token o usuario'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0002', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def cargar_mensajes(request):
    print "carga de mensajes"
    try:
        datos = json.loads(request.POST['data'])
        print datos
        try:
            if comprobar_usuario(datos):
                usuario_id = datos.get("usuario_id")
                usuario = get_object_or_None(User, pk=usuario_id)

                protectora_id = datos.get("id_protectora")
                protectora = get_object_or_None(Protectora, pk=protectora_id)
                protectora_usuario = protectora.admin.pk
                protectora_usuario = get_object_or_None(User, pk=protectora_usuario)

                conversacion = Conversacion.objects.filter(usuario=usuario)
                lista_conversaciones = []
                if conversacion is not None:
                    conversacion = conversacion.filter(protectora=protectora_usuario)
                    if conversacion is not None:
                        mensajes = Mensaje.objects.filter(conversacion=conversacion)
                        for mensaje in mensajes:
                            if mensaje.usuario.pk == usuario.pk:
                                emisario = "usuario"
                            else:
                                emisario = "protectora"

                            lista_conversaciones.append({
                                'pk': mensaje.pk,
                                'usuario': {
                                    'username': usuario.username,
                                    'nombre': usuario.first_name,
                                    'apellidos': usuario.last_name,
                                    'email': usuario.email,
                                    'telefono': usuario.datosextrauser.telefono,
                                    'direccion': usuario.datosextrauser.direccion,
                                    'codigo_postal': usuario.datosextrauser.cod_postal,
                                    'provincia': usuario.datosextrauser.provincia.provincia,
                                    'foto': str(usuario.datosextrauser.imagen)
                                },
                                'protectora': {
                                    'pk': protectora.pk,
                                    'nombre': protectora.nombre,
                                    'direccion': protectora.direccion,
                                    'codigo_postal': protectora.cod_postal,
                                    'provincia': protectora.provincia.provincia,
                                    'descripcion': protectora.descripcion
                                },
                                'mensaje': mensaje.mensaje,
                                'emisario': emisario,
                                'hora': str(mensaje.hora)
                            })

                response_data = {'result': 'ok',
                                 'message': 'listado de conversaciones',
                                 "lista_conversaciones": lista_conversaciones}

            else:
                response_data = {'result': 'error', 'message': 'error de token o usuario'}
            print response_data
        except:
            response_data = {'result': 'error', 'message': 'error de token o usuario'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0002', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def enviar_mensaje_protectora_de_usuario(request):
    print "enviando mensaje a la protectora y devuelvo mensaje"
    try:
        datos = json.loads(request.POST['data'])
        try:
            if comprobar_usuario(datos):
                protectora_id = datos.get('protectora')
                usuario_id = datos.get('usuario_id')
                mensaje = datos.get('message')
                print mensaje
                try:
                    protectora_objeto = get_object_or_None(Protectora, pk=protectora_id)
                    usuario_objeto = get_object_or_None(User, pk=usuario_id)
                except:
                    response_data = {'result': 'error', 'message': 'Protectora o Usuario no encontrados'}
                    return http.HttpResponse(json.dumps(response_data), content_type="application/json")

                admin_protectora = protectora_objeto.admin.pk

                usuario_objeto2 = get_object_or_None(User, pk=admin_protectora)

                conversacion = Conversacion.objects.filter(usuario=usuario_objeto)
                if conversacion is not None:
                    conversacion = conversacion.filter(protectora=usuario_objeto2)
                    if conversacion is not None:
                        conversacion = get_object_or_None(Conversacion,
                                                          protectora=usuario_objeto2,
                                                          usuario=usuario_objeto)
                    else:
                        conversacion = Conversacion.objects.create(protectora=usuario_objeto2,
                                                                   usuario=usuario_objeto)
                        conversacion.save()
                else:
                    conversacion = Conversacion.objects.create(protectora=usuario_objeto2,
                                                               usuario=usuario_objeto)
                    conversacion.save()

                mensaje = Mensaje.objects.create(usuario=usuario_objeto,
                                                 mensaje=mensaje,
                                                 conversacion=conversacion)
                mensaje.save()

                if mensaje.usuario.username == usuario_objeto.username:
                    emisario = "usuario"
                else:
                    emisario = "protectora"

                lista_conversaciones = []
                lista_conversaciones.append({
                    'pk': mensaje.pk,
                    'usuario': {
                        'username': usuario_objeto.username,
                        'nombre': usuario_objeto.first_name,
                        'apellidos': usuario_objeto.last_name,
                        'email': usuario_objeto.email,
                        'telefono': usuario_objeto.datosextrauser.telefono,
                        'direccion': usuario_objeto.datosextrauser.direccion,
                        'codigo_postal': usuario_objeto.datosextrauser.cod_postal,
                        'provincia': usuario_objeto.datosextrauser.provincia.provincia,
                        'foto': str(usuario_objeto.datosextrauser.imagen)
                    },
                    'protectora': {
                        'pk': protectora_objeto.pk,
                        'nombre': protectora_objeto.nombre,
                        'direccion': protectora_objeto.direccion,
                        'codigo_postal': protectora_objeto.cod_postal,
                        'provincia': protectora_objeto.provincia.provincia,
                        'descripcion': protectora_objeto.descripcion
                    },
                    'mensaje': mensaje.mensaje,
                    'emisario': emisario,
                    'hora': str(mensaje.hora)
                })

                response_data = {'result': 'ok',
                                 'message': 'mensaje enviado',
                                 'lista_conversaciones': lista_conversaciones}
            else:
                response_data = {'result': 'error', 'message': 'error de token o usuario'}
        except:
            response_data = {'result': 'error', 'message': 'error de token o usuario'}
        print response_data
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0002', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")
