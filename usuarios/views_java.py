# -*- encoding: utf-8 -*-
from django.core.mail import send_mail

from comunidad.models import Provincia
from configuracion import settings
from utilidades.contrasena import contrasena_generator

__author__ = 'brian'

import django.contrib.auth as auth
import django.http as http
from annoying.functions import get_object_or_None
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
import datetime
from utilidades import Token, enviarmail
from usuarios.models import Tokenregister, DatosExtraUser
from django.contrib.auth.models import User


# definicion para conseguir el usuario de django a partir del token
def get_userdjango_by_token(datos):
    token = datos.get('token')
    user_token = Tokenregister.objects.get(token=token)
    return user_token.user


# definicion para conseguir el usuario de django a partir del id de usuario
def get_userdjango_by_id(datos):
    userdjango_id = datos.get('usuario_id')
    userdjango = get_object_or_None(User, pk=userdjango_id)
    return userdjango


# definicion para comprobar el usuario
def comprobar_usuario(datos):
    userdjango = get_userdjango_by_id(datos)
    user_token = get_userdjango_by_token(datos)

    if (user_token is not None) and (userdjango is not None):
        if user_token == userdjango:
            return True
        else:
            return False


# definicion para loguear un usuario desde la aplicación java
@csrf_exempt
def login(request):
    print "Login"
    try:

        datos = json.loads(request.POST['data'])

        us = datos.get('usuario').lower()
        password = datos.get('password')

        if (us is None and password is None) or (us == "" and password == ""):
            response_data = {'result': 'error', 'message': 'Falta el usuario y el password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if us is None or us == "":
            response_data = {'result': 'error', 'message': 'Falta el usuario'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if password is None or password == "":
            response_data = {'result': 'error', 'message': 'Falta el password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        user = auth.authenticate(username=us, password=password)

        if user is not None:
            if user.is_active:
                user_token = get_object_or_None(Tokenregister, user=user)
                print user_token
                if user_token is None:
                    print "is none"
                    token1 = str(user.id) + "_" + Token.id_generator()
                    tokenform = Tokenregister(token=token1, user=user)
                    tokenform.save()
                    user_token = get_object_or_None(Tokenregister, user=user)
                    response_data = {'result': 'ok', 'message': 'Usuario logueado', 'token': user_token.token,
                                     'usuario': user.username,
                                     'nombre': user.first_name,
                                     }
                else:
                    # user_token.date = datetime.datetime.now()
                    # user_token.token = str(user.id) + "_" + Token.id_generator()
                    # user_token.save()
                    response_data = {
                        'result': 'error',
                        'message': 'Ya hay una sesion iniciada. Cierra primero las otras',
                    }

                return http.HttpResponse(json.dumps(response_data), content_type="application/json")

            else:
                response_data = {'result': 'error', 'message': 'Usuario no activo'}
                return http.HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data = {'result': 'error', 'message': 'Usuario no válido'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0001', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


# definicion para logear un usuario desde la aplicación java
@csrf_exempt
def logout(request):
    print "Logout"
    try:
        datos = json.loads(request.POST['data'])
        if comprobar_usuario(datos):
            userdjango = get_userdjango_by_token(datos)

            user_token = get_object_or_None(Tokenregister, user=userdjango)
            if user_token is None:
                response_data = {'result': 'ok', 'message': 'Usuario ya deslogueado'}
            else:

                user_token.delete()
                response_data = {'result': 'ok', 'message': 'Usuario ya deslogueado'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0002', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def recuperar_contrasena(request):
    try:
        try:
            # import pdb
            # pdb.set_trace()
            datos = json.loads(request.POST['data'])
            username = datos.get('usuario')

        except Exception as e:
            username = request.POST['usuario']

        # if token != "" and comprobar_usuario2(token, userdjango_id):
        userdjango = get_object_or_None(User, username=username)
        if userdjango is not None:
            nueva_contrasena = contrasena_generator()
            print nueva_contrasena + " - " + userdjango.email
            userdjango.set_password(nueva_contrasena)
            userdjango.save()
            enviarmail.enviar_email("Contraseña nueva", "Se ha generado una nueva contraseña: " + nueva_contrasena,
                                    "Se ha generado una nueva contraseña: " + nueva_contrasena, [userdjango.email, ])
            response_data = {'result': 'ok', 'message': 'usuario existente'}
        else:
            response_data = {'result': 'error', 'message': 'usuario no existente'}

        print response_data
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


    except Exception as e:
        response_data = {'errorcode': 'U0003', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


# definicion para comprobar el token
@csrf_exempt
def comprobar_token(request):
    print "Comprobando token"
    try:
        datos = json.loads(request.POST['data'])
        token = datos.get('token')
        if token != "" and comprobar_usuario(datos):
            response_data = {'result': 'ok', 'message': 'Usuario logueado'}

        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0003', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def get_perfil(request):
    print "buscando perfil"
    try:
        datos = json.loads(request.POST['data'])

        if comprobar_usuario(datos):
            userdjango = get_userdjango_by_token(datos)

            response_data = {'result': 'ok', 'message': 'Perfil de usuario',
                             'email': userdjango.email,
                             'username': userdjango.username,
                             'nombre': userdjango.first_name,
                             'apellidos': userdjango.last_name}

        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0004', 'result': 'error', 'message': 'Error en perfil de usuario: ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


# metodo para que un usuario pueda ver su perfil, necesario estar loegueado y pasar su id y token
@csrf_exempt
def cambiar_pass(request):
    print "cambiando pass"
    try:
        datos = json.loads(request.POST['data'])
        antiguapass = datos.get('antigua')
        nuevapass = datos.get('nueva')

        if comprobar_usuario(datos):
            userdjango = get_userdjango_by_token(datos)
            if userdjango.check_password(antiguapass):
                userdjango.set_password(nuevapass)
                userdjango.save()
                token = get_object_or_None(Tokenregister, user=userdjango)
                token.delete()
                response_data = {'result': 'ok', 'message': 'Contraseña cambiada'}
            else:
                response_data = {'result': 'error', 'message': 'Contraseña antigua incorrecta'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0005', 'result': 'error', 'message': 'Error en perfil de usuario: ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


# metodo para que un usuario pueda ver su perfil, necesario estar loegueado y pasar su id y token
@csrf_exempt
def cambiar_email(request):
    print "cambiando pass"
    try:
        datos = json.loads(request.POST['data'])
        emailantiguo = datos.get('antiguo')
        emailnuevo = datos.get('nuevo')

        if comprobar_usuario(datos):
            userdjango = get_userdjango_by_token(datos)
            usuarios_email = User.objects.filter(email=emailnuevo)
            print userdjango.email
            print emailantiguo
            if userdjango.email == emailantiguo:
                if usuarios_email.count() == 0:
                    userdjango.email = emailnuevo
                    userdjango.save()
                    token = get_object_or_None(Tokenregister, user=userdjango)
                    token.delete()
                    response_data = {'result': 'ok', 'message': 'Email cambiado'}
                else:
                    response_data = {'result': 'error', 'message': 'Ese email ya está registrado'}
            else:
                response_data = {'result': 'error', 'message': 'Email antiguo incorrecto'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0005', 'result': 'error',
                         'message': 'Error en perfil de usuario: ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


# definicion para registrar un usuario
@csrf_exempt
def registrar_usuario(request):
    print "registrando usuario"
    try:
        datos = json.loads(request.POST['data'])

        nombre = datos.get('usuario')
        email = datos.get('email')
        password = datos.get('password')
        provincia = datos.get('provincia')
        # Hago un filtro con el nombre de la provincia obtenida para obtener el objeto con la id.
        provincia_escogida = get_object_or_None(Provincia, provincia=provincia)
        id_provincia = provincia_escogida.pk
        print id_provincia

        if (nombre is None and email is None and password is None) or (nombre == "" and password == "" and email == ""):
            response_data = {'result': 'error', 'message': 'Falta el nombre usuario, email y password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if nombre is None or nombre == "":
            response_data = {'result': 'error', 'message': 'Falta el nombre de usuario'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if password is None or password == "":
            response_data = {'result': 'error', 'message': 'Falta el password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if email is None or email == "":
            response_data = {'result': 'error', 'message': 'Falta el email'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        usuarios = User.objects.filter(username=nombre)
        usuarios_email = User.objects.filter(email=email)

        if usuarios.count() == 0:
            if usuarios_email.count() == 0:
                user = User.objects.create(username=nombre, email=email)
                user.set_password(password)
                usuario = DatosExtraUser.objects.create(user=user, direccion="", provincia=provincia_escogida,
                                                        cod_postal="", telefono="")
                user.save()
                usuario.save()
                enviarmail.enviar_email("Registro", "Se ha registrado con éxito en Mímame",
                                        "Se ha registrado con éxito en Mímame",
                                        [user.email, ])
                response_data = {'result': 'ok', 'message': 'Usuario creado correctamente'}
            else:
                response_data = {'result': 'error', 'message': 'Este email ya existe'}
        else:
            response_data = {'result': 'error', 'message': 'Este nombre de usuario ya existe'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0005', 'result': 'error', 'message': 'Error en crear usuario. ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def cambiar_datos(request):
    print "cambiando datos personales"
    try:
        datos = json.loads(request.POST['data'])
        if comprobar_usuario(datos):
            userdjango = get_userdjango_by_token(datos)
            userdjango.first_name = datos.get('nombre')
            userdjango.last_name = datos.get('apellidos')
            userdjango.datosextrauser.direccion = datos.get('direccion')
            provincia = get_object_or_None(Provincia, provincia=datos.get('provincia'))
            userdjango.datosextrauser.provincia = provincia
            userdjango.datosextrauser.telefono = datos.get('telefono')
            userdjango.datosextrauser.cod_postal = datos.get('codigo_postal')
            userdjango.save()
            userdjango.datosextrauser.save()
            response_data = {'result': 'ok', 'message': 'Datos cambiados'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0007', 'result': 'error', 'message': 'Error en perfil de usuario: ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def cargar_usuario(request):
    print "Cargando usuario"
    try:
        datos = json.loads(request.POST['data'])

        try:
            token = datos.get('token')
            usuario_id = datos.get('usuario_id')
            if comprobar_usuario(datos):
                userdjango = get_object_or_None(User, pk=usuario_id)

                if userdjango is not None:

                    usuario = {
                        "username": userdjango.username,
                        "nombre": userdjango.first_name,
                        "apellidos": userdjango.last_name,
                        "email": userdjango.email,
                        "telefono": userdjango.datosextrauser.telefono,
                        "direccion": userdjango.datosextrauser.direccion,
                        "codigo_postal": userdjango.datosextrauser.cod_postal,
                        "provincia": userdjango.datosextrauser.provincia.provincia,
                        "foto": str(userdjango.datosextrauser.imagen)
                    }
                    response_data = {
                        'result': 'ok',
                        'message': 'datos del usuario',
                        'usuario': usuario
                    }
                else:
                    response_data = {'result': 'error',
                                     'message': 'ha habido un error, intentelo de nuevo'}
            else:
                response_data = {'result': 'error',
                                 'message': 'ha habido un error, intentelo de nuevo'}

        except:
            response_data = {'result': 'error', 'message': 'error de token o usuario'}

        print response_data
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0007', 'result': 'error', 'message': 'Error en perfil de usuario: ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def get_usuarios(request):
    print "buscando usuarios"
    try:
        # datos = json.loads(request.POST['data'])

        # if comprobar_usuario(datos):
        response_data = {'result': 'ok', 'message': 'Listado de usuarios', 'usuarios': []}
        usuarios = User.objects.all().order_by('id')
        for a in usuarios:
            response_data['usuarios'].append({'pk': a.pk, 'username': a.username, 'email': a.email, })

        # else:
        #     response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0006', 'result': 'error',
                         'message': 'Error en busqueda de usuarios : ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def set_foto(request):
    print "eligiendo foto"
    # import pdb
    # pdb.set_trace()
    try:
        try:
            datos = json.loads(request.POST['data'])
            token = datos.get('token')

        except Exception as e:
            token = request.POST['token']

        if comprobar_usuario(datos):
            user = get_userdjango_by_token(datos)
            archivo = request.FILES['file']
            tama = archivo.size
            # print "-----------------------------------------------------"
            # print ("TAMAÑO",tama)
            if tama <= 2000000:
                extension = archivo.name.split('.')[-1]
                lista = ['jpg', 'JPG', 'png', 'PNG']
                if extension in lista:
                    nombre = 'usuario' + str(user.pk) + '.' + extension
                    lpath = settings.MEDIA_IMAGE + "perfiles/" + nombre
                    destino = open(lpath, 'wb+')
                    for chunk in archivo.chunks():
                        destino.write(chunk)
                    destino.close()

                    user.datosextrauser.imagen = "/imagenes/perfiles/" + nombre
                    user.datosextrauser.save()
                response_data = {'result': 'ok',
                                 'message': 'Foto subida correctamente'}
            else:
                response_data = {'result': 'error',
                                 'message': 'Foto demasiado pesada'}

        else:
            response_data = {'result': 'error', 'message': 'Sesiones no cargadas'}

        print response_data

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        print e
        response_data = {'errorcode': 'U0006', 'result': 'error',
                         'message': 'Error en busqueda de sesiones : ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

# realizar este get_usuarios en Centros y Sesiones. Lo unico que varia es el try con los datos que cada uno pide
# el de centros realizarlo en view_java de Centros
