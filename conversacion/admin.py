from django.contrib import admin

# Register your models here.
from conversacion.models import Conversacion, Mensaje

admin.site.register(Mensaje)
admin.site.register(Conversacion)
