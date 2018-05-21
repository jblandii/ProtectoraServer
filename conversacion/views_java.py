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

                conversacion = Conversacion.objects.create(protectora=usuario_objeto2, usuario=usuario_objeto)
                conversacion.save()
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
