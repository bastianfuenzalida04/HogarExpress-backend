from django.contrib import admin

from .models import Pedido, DetallePedido


class DetallePedidoInline(
    admin.TabularInline
):
    model = DetallePedido
    extra = 0

    readonly_fields = (
        "producto",
        "nombre_producto",
        "precio_unitario",
        "cantidad",
        "subtotal",
    )


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "usuario",
        "estado",
        "subtotal",
        "costo_despacho",
        "total",
        "pago_confirmado",
        "fecha_creacion",
    )

    list_filter = (
        "estado",
        "pago_confirmado",
        "fecha_creacion",
    )

    search_fields = (
        "usuario__username",
        "usuario__email",
        "id",
    )

    list_editable = (
        "estado",
    )

    readonly_fields = (
        "usuario",
        "direccion",
        "subtotal",
        "costo_despacho",
        "total",
        "pago_confirmado",
        "fecha_creacion",
        "fecha_actualizacion",
    )

    inlines = [
        DetallePedidoInline
    ]


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):

    list_display = (
        "pedido",
        "nombre_producto",
        "precio_unitario",
        "cantidad",
        "subtotal",
    )

    search_fields = (
        "nombre_producto",
        "pedido__id",
    )