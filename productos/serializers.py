from rest_framework import serializers

from .models import Categoria, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    cantidad_productos = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = [
            "id",
            "nombre",
            "descripcion",
            "imagen",
            "activa",
            "cantidad_productos",
        ]

    def get_cantidad_productos(self, obj):
        return obj.productos.filter(activo=True).count()


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(
        source="categoria.nombre",
        read_only=True
    )

    disponible = serializers.ReadOnlyField()

    class Meta:
        model = Producto
        fields = [
            "id",
            "categoria",
            "categoria_nombre",
            "nombre",
            "descripcion",
            "precio",
            "stock",
            "imagen",
            "activo",
            "destacado",
            "disponible",
            "fecha_creacion",
            "fecha_actualizacion",
        ]