from rest_framework import serializers

from .models import Pedido, DetallePedido


class DetallePedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetallePedido

        fields = [
            "id",
            "producto",
            "nombre_producto",
            "precio_unitario",
            "cantidad",
            "subtotal",
        ]


class PedidoSerializer(serializers.ModelSerializer):

    detalles = DetallePedidoSerializer(
        many=True,
        read_only=True
    )

    estado_nombre = serializers.CharField(
        source="get_estado_display",
        read_only=True
    )

    direccion = serializers.SerializerMethodField()

    # Indica al frontend si el pedido
    # fue realizado como invitado.
    es_invitado = serializers.SerializerMethodField()

    class Meta:
        model = Pedido

        fields = [
            "id",
            "estado",
            "estado_nombre",
            "subtotal",
            "costo_despacho",
            "total",
            "pago_confirmado",
            "fecha_creacion",
            "fecha_actualizacion",
            "direccion",
            "detalles",
            "es_invitado",
        ]

    def get_es_invitado(self, obj):

        return obj.usuario is None

    def get_direccion(self, obj):

        # -------------------------------------------------
        # PEDIDO DE INVITADO
        # -------------------------------------------------

        if obj.direccion is None:

            return {
                "id": None,
                "nombre_direccion": (
                    obj.nombre_direccion
                ),
                "calle": obj.calle,
                "numero": obj.numero,
                "comuna": obj.comuna,
                "region": obj.region,
                "informacion_adicional": (
                    obj.informacion_adicional
                ),
            }

        # -------------------------------------------------
        # PEDIDO DE USUARIO REGISTRADO
        # -------------------------------------------------

        return {
            "id": obj.direccion.id,
            "nombre_direccion": (
                obj.direccion.nombre_direccion
            ),
            "calle": obj.direccion.calle,
            "numero": obj.direccion.numero,
            "comuna": obj.direccion.comuna,
            "region": obj.direccion.region,
            "informacion_adicional": (
                obj.direccion.informacion_adicional
            ),
        }