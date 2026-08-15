from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carrito.models import Carrito
from usuarios.models import Direccion

from .models import Pedido, DetallePedido
from .serializers import PedidoSerializer
from .emails import enviar_correo_pedido


COSTO_DESPACHO = 2990


class CrearPedidoAPIView(APIView):

    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):

        # =====================================================
        # ASEGURAR SESIÓN PARA INVITADOS
        # =====================================================

        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key

        invitado = request.data.get(
            "invitado",
            False
        )

        # =====================================================
        # USUARIO INVITADO
        # =====================================================

        if invitado and not request.user.is_authenticated:

            nombre = request.data.get(
                "nombre",
                ""
            ).strip()

            apellido = request.data.get(
                "apellido",
                ""
            ).strip()

            correo = request.data.get(
                "correo",
                ""
            ).strip()

            telefono = request.data.get(
                "telefono",
                ""
            ).strip()

            calle = request.data.get(
                "calle",
                ""
            ).strip()

            numero = request.data.get(
                "numero",
                ""
            ).strip()

            comuna = request.data.get(
                "comuna",
                ""
            ).strip()

            region = request.data.get(
                "region",
                ""
            ).strip()

            informacion_adicional = request.data.get(
                "informacion_adicional",
                ""
            ).strip()

            # -------------------------------------------------
            # VALIDACIONES
            # -------------------------------------------------

            if not nombre:
                return Response(
                    {
                        "error": "Debe ingresar su nombre."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not apellido:
                return Response(
                    {
                        "error": "Debe ingresar su apellido."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not correo:
                return Response(
                    {
                        "error": "Debe ingresar su correo."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not telefono:
                return Response(
                    {
                        "error": "Debe ingresar su teléfono."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not calle:
                return Response(
                    {
                        "error": "Debe ingresar la calle."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not numero:
                return Response(
                    {
                        "error": "Debe ingresar el número."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not comuna:
                return Response(
                    {
                        "error": "Debe ingresar la comuna."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not region:
                return Response(
                    {
                        "error": "Debe ingresar la región."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # -------------------------------------------------
            # OBTENER CARRITO DEL INVITADO
            # -------------------------------------------------

            carrito = Carrito.objects.filter(
                session_key=session_key,
                usuario=None
            ).first()

            if not carrito:

                return Response(
                    {
                        "error": "No existe un carrito de invitado."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # -------------------------------------------------
            # OBTENER PRODUCTOS
            # -------------------------------------------------

            items = carrito.items.select_related(
                "producto"
            )

            if not items.exists():

                return Response(
                    {
                        "error": "El carrito está vacío."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            subtotal = 0

            for item in items:

                producto = item.producto

                if not producto.activo:

                    return Response(
                        {
                            "error": (
                                f"El producto "
                                f"{producto.nombre} "
                                f"ya no está disponible."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if item.cantidad > producto.stock:

                    return Response(
                        {
                            "error": (
                                f"No hay suficiente stock "
                                f"de {producto.nombre}."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                subtotal += (
                    producto.precio *
                    item.cantidad
                )

            total = subtotal + COSTO_DESPACHO

            # -------------------------------------------------
            # CREAR PEDIDO DE INVITADO
            # -------------------------------------------------

            pedido = Pedido.objects.create(

                usuario=None,

                session_key=session_key,

                direccion=None,

                nombre_comprador=nombre,

                apellido_comprador=apellido,

                correo_comprador=correo,

                telefono_comprador=telefono,

                nombre_direccion="Dirección de despacho",

                calle=calle,

                numero=numero,

                comuna=comuna,

                region=region,

                informacion_adicional=(
                    informacion_adicional
                ),

                subtotal=subtotal,

                costo_despacho=COSTO_DESPACHO,

                total=total,

                pago_confirmado=True,

                estado="recibido",
            )

            # -------------------------------------------------
            # DETALLES
            # -------------------------------------------------

            for item in items:

                producto = item.producto

                DetallePedido.objects.create(

                    pedido=pedido,

                    producto=producto,

                    nombre_producto=producto.nombre,

                    precio_unitario=producto.precio,

                    cantidad=item.cantidad,

                    subtotal=(
                        producto.precio *
                        item.cantidad
                    )
                )

                producto.stock -= item.cantidad

                producto.save(
                    update_fields=["stock"]
                )

            # -------------------------------------------------
            # VACIAR CARRITO
            # -------------------------------------------------

            carrito.items.all().delete()

            # -------------------------------------------------
            # ENVIAR CORREO DE CONFIRMACIÓN
            # -------------------------------------------------

            transaction.on_commit(
                lambda: enviar_correo_pedido(pedido)
            )

            return Response(
                {
                    "mensaje": "Pedido creado correctamente.",
                    "pedido": PedidoSerializer(
                        pedido
                    ).data
                },
                status=status.HTTP_201_CREATED
            )

        # =====================================================
        # USUARIO REGISTRADO
        # =====================================================

        if not request.user.is_authenticated:

            return Response(
                {
                    "error": (
                        "Debe iniciar sesión "
                        "para realizar esta compra."
                    )
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        direccion_id = request.data.get(
            "direccion_id"
        )

        if not direccion_id:

            return Response(
                {
                    "error": (
                        "Debe seleccionar "
                        "una dirección."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        direccion = get_object_or_404(
            Direccion,
            id=direccion_id,
            usuario=request.user
        )

        carrito = Carrito.objects.filter(
            usuario=request.user
        ).first()

        if not carrito:

            return Response(
                {
                    "error": "No existe un carrito."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        items = carrito.items.select_related(
            "producto"
        )

        if not items.exists():

            return Response(
                {
                    "error": "El carrito está vacío."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        subtotal = 0

        for item in items:

            producto = item.producto

            if not producto.activo:

                return Response(
                    {
                        "error": (
                            f"El producto "
                            f"{producto.nombre} "
                            f"ya no está disponible."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if item.cantidad > producto.stock:

                return Response(
                    {
                        "error": (
                            f"No hay suficiente stock "
                            f"de {producto.nombre}."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            subtotal += (
                producto.precio *
                item.cantidad
            )

        total = subtotal + COSTO_DESPACHO

        # -------------------------------------------------
        # CREAR PEDIDO DE USUARIO REGISTRADO
        # -------------------------------------------------

        pedido = Pedido.objects.create(

            usuario=request.user,

            direccion=direccion,

            nombre_comprador=(
                request.user.first_name
            ),

            apellido_comprador=(
                request.user.last_name
            ),

            correo_comprador=(
                request.user.email
            ),

            telefono_comprador=(
                getattr(
                    request.user,
                    "telefono",
                    ""
                )
            ),

            nombre_direccion=(
                direccion.nombre_direccion
            ),

            calle=direccion.calle,

            numero=direccion.numero,

            comuna=direccion.comuna,

            region=direccion.region,

            informacion_adicional=(
                direccion.informacion_adicional
            ),

            subtotal=subtotal,

            costo_despacho=COSTO_DESPACHO,

            total=total,

            pago_confirmado=True,

            estado="recibido",
        )

        # -------------------------------------------------
        # DETALLES
        # -------------------------------------------------

        for item in items:

            producto = item.producto

            DetallePedido.objects.create(

                pedido=pedido,

                producto=producto,

                nombre_producto=producto.nombre,

                precio_unitario=producto.precio,

                cantidad=item.cantidad,

                subtotal=(
                    producto.precio *
                    item.cantidad
                )
            )

            producto.stock -= item.cantidad

            producto.save(
                update_fields=["stock"]
            )

        # -------------------------------------------------
        # VACIAR CARRITO
        # -------------------------------------------------

        carrito.items.all().delete()

        # -------------------------------------------------
        # ENVIAR CORREO DE CONFIRMACIÓN
        # -------------------------------------------------

        transaction.on_commit(
            lambda: enviar_correo_pedido(pedido)
        )

        return Response(
            {
                "mensaje": "Pedido creado correctamente.",
                "pedido": PedidoSerializer(
                    pedido
                ).data
            },
            status=status.HTTP_201_CREATED
        )


class MisPedidosAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        pedidos = Pedido.objects.filter(
            usuario=request.user
        ).prefetch_related(
            "detalles"
        ).select_related(
            "direccion"
        )

        return Response(
            PedidoSerializer(
                pedidos,
                many=True
            ).data
        )


class PedidoDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        pedido = get_object_or_404(
            Pedido,
            id=pk
        )

        # =====================================================
        # USUARIO REGISTRADO
        # =====================================================

        if request.user.is_authenticated:

            if pedido.usuario != request.user:

                return Response(
                    {
                        "error": (
                            "No tienes permiso "
                            "para ver este pedido."
                        )
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        # =====================================================
        # INVITADO
        # =====================================================

        else:

            if (
                not request.session.session_key
                or pedido.session_key
                != request.session.session_key
            ):

                return Response(
                    {
                        "error": (
                            "No tienes permiso "
                            "para ver este pedido."
                        )
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        return Response(
            PedidoSerializer(
                pedido
            ).data
        )
class RepetirPedidoAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):

        # =====================================================
        # BUSCAR PEDIDO DEL USUARIO
        # =====================================================

        pedido = get_object_or_404(
            Pedido,
            id=pk,
            usuario=request.user
        )

        # =====================================================
        # OBTENER DETALLES DEL PEDIDO
        # =====================================================

        detalles = pedido.detalles.select_related(
            "producto"
        )

        if not detalles.exists():

            return Response(
                {
                    "error": "Este pedido no contiene productos."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =====================================================
        # OBTENER CARRITO DEL USUARIO
        # =====================================================

        carrito, created = Carrito.objects.get_or_create(
            usuario=request.user
        )

        # =====================================================
        # VALIDAR TODOS LOS PRODUCTOS ANTES DE MODIFICAR
        # =====================================================

        for detalle in detalles:

            producto = detalle.producto

            if not producto.activo:

                return Response(
                    {
                        "error": (
                            f"El producto "
                            f"{producto.nombre} "
                            f"ya no está disponible."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            item_existente = carrito.items.filter(
                producto=producto
            ).first()

            cantidad_actual = (
                item_existente.cantidad
                if item_existente
                else 0
            )

            cantidad_final = (
                cantidad_actual +
                detalle.cantidad
            )

            if cantidad_final > producto.stock:

                return Response(
                    {
                        "error": (
                            f"No hay suficiente stock "
                            f"de {producto.nombre}. "
                            f"Stock disponible: "
                            f"{producto.stock}."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # =====================================================
        # AGREGAR PRODUCTOS AL CARRITO
        # =====================================================

        for detalle in detalles:

            producto = detalle.producto

            item, created = (
                carrito.items.get_or_create(
                    producto=producto,
                    defaults={
                        "cantidad": detalle.cantidad
                    }
                )
            )

            if not created:

                item.cantidad += detalle.cantidad
                item.save()

        # =====================================================
        # RESPUESTA
        # =====================================================

        return Response(
            {
                "mensaje": (
                    "Los productos del pedido "
                    "fueron agregados al carrito."
                ),
                "carrito": {
                    "id": carrito.id,
                    "total_items": carrito.total_items,
                    "subtotal": carrito.subtotal,
                }
            },
            status=status.HTTP_200_OK
        )