from django.contrib import admin
from .models import Usuario, Evento, RegistroEvento

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Evento)
admin.site.register(RegistroEvento)