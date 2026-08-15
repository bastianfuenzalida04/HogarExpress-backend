from django.contrib import admin

from .models import Carrito, ItemCarrito


class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "total_items",
        "subtotal",
        "fecha_actualizacion",
    )

    inlines = [
        ItemCarritoInline
    ]


@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = (
        "carrito",
        "producto",
        "cantidad",
        "subtotal",
        "fecha_agregado",
    )

    search_fields = (
        "producto__nombre",
        "carrito__usuario__username",
    )