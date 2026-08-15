from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from productos.models import Producto

from .models import Carrito, ItemCarrito
from .serializers import CarritoSerializer


def obtener_carrito(request):
    """
    Obtiene el carrito correspondiente a la petición.

    Usuario registrado:
        Busca el carrito asociado al usuario.

    Usuario invitado:
        Busca el carrito asociado a la sesión.
    """

    # =====================================================
    # USUARIO REGISTRADO
    # =====================================================

    if request.user.is_authenticated:

        carrito, created = Carrito.objects.get_or_create(
            usuario=request.user
        )

        return carrito

    # =====================================================
    # USUARIO INVITADO
    # =====================================================

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    carrito, created = Carrito.objects.get_or_create(
        session_key=session_key,
        usuario=None,
    )

    return carrito


class CarritoAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        carrito = obtener_carrito(request)

        return Response(
            CarritoSerializer(
                carrito,
                context={"request": request}
            ).data
        )


class AgregarCarritoAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        producto_id = request.data.get(
            "producto_id"
        )

        cantidad = request.data.get(
            "cantidad",
            1
        )

        if not producto_id:

            return Response(
                {
                    "error": "Debe indicar el producto."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            cantidad = int(cantidad)

        except (TypeError, ValueError):

            return Response(
                {
                    "error": "La cantidad debe ser un número."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if cantidad <= 0:

            return Response(
                {
                    "error": "La cantidad debe ser mayor a 0."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        producto = get_object_or_404(
            Producto,
            id=producto_id,
            activo=True
        )

        if cantidad > producto.stock:

            return Response(
                {
                    "error": "No hay suficiente stock."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        carrito = obtener_carrito(request)

        item, created = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={
                "cantidad": cantidad
            }
        )

        if not created:

            nueva_cantidad = (
                item.cantidad + cantidad
            )

            if nueva_cantidad > producto.stock:

                return Response(
                    {
                        "error": "No hay suficiente stock."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            item.cantidad = nueva_cantidad
            item.save()

        return Response(
            CarritoSerializer(
                carrito,
                context={"request": request}
            ).data,
            status=status.HTTP_200_OK
        )


class ActualizarItemCarritoAPIView(APIView):

    permission_classes = [AllowAny]

    def put(self, request, pk):

        carrito = obtener_carrito(request)

        item = get_object_or_404(
            ItemCarrito,
            id=pk,
            carrito=carrito
        )

        cantidad = request.data.get(
            "cantidad"
        )

        try:

            cantidad = int(cantidad)

        except (TypeError, ValueError):

            return Response(
                {
                    "error": "La cantidad debe ser un número."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if cantidad <= 0:

            item.delete()

            return Response(
                CarritoSerializer(
                    carrito,
                    context={"request": request}
                ).data
            )

        if cantidad > item.producto.stock:

            return Response(
                {
                    "error": "No hay suficiente stock."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        item.cantidad = cantidad
        item.save()

        return Response(
            CarritoSerializer(
                carrito,
                context={"request": request}
            ).data
        )


class EliminarItemCarritoAPIView(APIView):

    permission_classes = [AllowAny]

    def delete(self, request, pk):

        carrito = obtener_carrito(request)

        item = get_object_or_404(
            ItemCarrito,
            id=pk,
            carrito=carrito
        )

        item.delete()

        return Response(
            CarritoSerializer(
                carrito,
                context={"request": request}
            ).data,
            status=status.HTTP_200_OK
        )


class VaciarCarritoAPIView(APIView):

    permission_classes = [AllowAny]

    def delete(self, request):

        carrito = obtener_carrito(request)

        carrito.items.all().delete()

        return Response(
            {
                "mensaje": "Carrito vaciado correctamente."
            },
            status=status.HTTP_200_OK
        )