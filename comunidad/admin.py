from django.contrib import admin

# Register your models here.
from comunidad.models import Provincia, ComunidadAutonoma

admin.site.register(Provincia)
admin.site.register(ComunidadAutonoma)
