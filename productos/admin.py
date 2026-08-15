from django.contrib import admin
from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa", "fecha_creacion")
    list_filter = ("activa",)
    search_fields = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "categoria",
        "precio",
        "stock",
        "activo",
        "destacado",
    )

    list_filter = (
        "categoria",
        "activo",
        "destacado",
    )

    search_fields = (
        "nombre",
        "descripcion",
    )

    list_editable = (
        "precio",
        "stock",
        "activo",
        "destacado",
    )