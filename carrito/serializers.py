from rest_framework import serializers

from .models import Carrito, ItemCarrito


class ItemCarritoSerializer(serializers.ModelSerializer):

    producto_nombre = serializers.CharField(
        source="producto.nombre",
        read_only=True
    )

    producto_precio = serializers.DecimalField(
        source="producto.precio",
        max_digits=10,
        decimal_places=0,
        read_only=True
    )

    producto_imagen = serializers.ImageField(
        source="producto.imagen",
        read_only=True
    )

    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = ItemCarrito

        fields = [
            "id",
            "producto",
            "producto_nombre",
            "producto_precio",
            "producto_imagen",
            "cantidad",
            "subtotal",
        ]


class CarritoSerializer(serializers.ModelSerializer):

    items = ItemCarritoSerializer(
        many=True,
        read_only=True
    )

    subtotal = serializers.ReadOnlyField()

    total_items = serializers.ReadOnlyField()

    class Meta:
        model = Carrito

        fields = [
            "id",
            "items",
            "total_items",
            "subtotal",
            "fecha_actualizacion",
        ]