from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carrito.models import Carrito, ItemCarrito

from .models import Direccion
from .serializers import (
    RegistroSerializer,
    LoginSerializer,
    UsuarioSerializer,
    DireccionSerializer,
)

from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator


class RegistroAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegistroSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    "mensaje": "Usuario registrado correctamente.",
                    "usuario": UsuarioSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@method_decorator(
    ensure_csrf_cookie,
    name="dispatch"
)
class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = serializer.validated_data[
            "username"
        ]

        password = serializer.validated_data[
            "password"
        ]

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:

            return Response(
                {
                    "error": "Usuario o contraseña incorrectos."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # ==================================================
        # GUARDAR LA SESIÓN DEL INVITADO
        # ==================================================

        session_key = request.session.session_key

        # ==================================================
        # TRANSFERIR CARRITO DE INVITADO
        # ==================================================

        if session_key:

            carrito_invitado = (
                Carrito.objects.filter(
                    session_key=session_key,
                    usuario=None
                )
                .first()
            )

            if carrito_invitado:

                # Obtener o crear el carrito
                # perteneciente al usuario.
                carrito_usuario, created = (
                    Carrito.objects.get_or_create(
                        usuario=user
                    )
                )

                # ------------------------------------------
                # Pasar cada producto al carrito del usuario
                # ------------------------------------------

                for item_invitado in (
                    carrito_invitado.items.select_related(
                        "producto"
                    )
                ):

                    item_usuario, item_created = (
                        ItemCarrito.objects.get_or_create(
                            carrito=carrito_usuario,
                            producto=item_invitado.producto,
                            defaults={
                                "cantidad": item_invitado.cantidad
                            }
                        )
                    )

                    if not item_created:

                        nueva_cantidad = (
                            item_usuario.cantidad
                            + item_invitado.cantidad
                        )

                        # No superar el stock disponible.
                        nueva_cantidad = min(
                            nueva_cantidad,
                            item_invitado.producto.stock
                        )

                        item_usuario.cantidad = (
                            nueva_cantidad
                        )

                        item_usuario.save()

                # ------------------------------------------
                # Eliminar el carrito de invitado
                # ------------------------------------------

                carrito_invitado.delete()

        # ==================================================
        # INICIAR SESIÓN
        # ==================================================

        login(
            request,
            user
        )

        return Response(
            {
                "mensaje": "Inicio de sesión exitoso.",
                "usuario": UsuarioSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        logout(request)

        return Response(
            {
                "mensaje": "Sesión cerrada correctamente."
            },
            status=status.HTTP_200_OK,
        )


class UsuarioActualAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(
            UsuarioSerializer(
                request.user
            ).data
        )


class DireccionesAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        direcciones = Direccion.objects.filter(
            usuario=request.user
        )

        serializer = DireccionSerializer(
            direcciones,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(self, request):

        serializer = DireccionSerializer(
            data=request.data
        )

        if serializer.is_valid():

            direccion = serializer.save(
                usuario=request.user
            )

            return Response(
                DireccionSerializer(
                    direccion
                ).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class DireccionDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):

        try:

            return Direccion.objects.get(
                pk=pk,
                usuario=user
            )

        except Direccion.DoesNotExist:

            return None

    def get(self, request, pk):

        direccion = self.get_object(
            pk,
            request.user
        )

        if direccion is None:

            return Response(
                {
                    "error": "Dirección no encontrada."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            DireccionSerializer(
                direccion
            ).data
        )

    def put(self, request, pk):

        direccion = self.get_object(
            pk,
            request.user
        )

        if direccion is None:

            return Response(
                {
                    "error": "Dirección no encontrada."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DireccionSerializer(
            direccion,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):

        direccion = self.get_object(
            pk,
            request.user
        )

        if direccion is None:

            return Response(
                {
                    "error": "Dirección no encontrada."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        direccion.delete()

        return Response(
            {
                "mensaje": "Dirección eliminada correctamente."
            },
            status=status.HTTP_204_NO_CONTENT,
        )
