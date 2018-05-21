from django.contrib import admin

# Register your models here.
# admin.site.register(Tokenregister)
from protectora.models import Animal, RedSocial, Adopcion, Protectora, MeGusta, ImagenAnimal, RazaAnimal, \
    ImagenProtectora

admin.site.register(RedSocial)
admin.site.register(Adopcion)
admin.site.register(Protectora)
admin.site.register(RazaAnimal)
admin.site.register(MeGusta)
admin.site.register(ImagenAnimal)
admin.site.register(ImagenProtectora)
admin.site.register(Animal)
