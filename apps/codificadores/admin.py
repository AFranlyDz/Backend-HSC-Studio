from django.contrib import admin

from apps.codificadores.models import Codificadores

# Register your models here.


@admin.register(Codificadores)
class CodificadoresAdmin(admin.ModelAdmin):

    fields = ["nombre", "nombre_corto", "descripcion", "clasificacion"]

    list_display = ["id", "nombre", "nombre_corto", "clasificacion"]
