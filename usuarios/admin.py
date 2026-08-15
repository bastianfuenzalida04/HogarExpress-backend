from django.contrib import admin
from .models import Perfil, Direccion


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "apellido",
        "usuario",
        "telefono",
        "fecha_creacion",
    )

    search_fields = (
        "nombre",
        "apellido",
        "usuario__username",
        "usuario__email",
    )


@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "nombre_direccion",
        "calle",
        "numero",
        "comuna",
        "region",
        "principal",
    )

    list_filter = (
        "region",
        "comuna",
        "principal",
    )

    search_fields = (
        "usuario__username",
        "calle",
        "comuna",
    )