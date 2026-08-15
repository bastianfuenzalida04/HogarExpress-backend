from django.contrib.auth.models import User
from django.db import models

from productos.models import Producto
from usuarios.models import Direccion


class Pedido(models.Model):

    ESTADOS = [
        ("recibido", "Pedido recibido"),
        ("preparando", "Preparando pedido"),
        ("en_camino", "En camino"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]

    # Usuario registrado.
    # Puede ser NULL cuando la compra es como invitado.
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="pedidos",
        null=True,
        blank=True,
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
    )

    # Dirección guardada del usuario.
    # En una compra como invitado será NULL.
    direccion = models.ForeignKey(
        Direccion,
        on_delete=models.PROTECT,
        related_name="pedidos",
        null=True,
        blank=True,
    )

    # -------------------------------------------------
    # DATOS DEL COMPRADOR
    # -------------------------------------------------

    nombre_comprador = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    apellido_comprador = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    correo_comprador = models.EmailField(
        blank=True,
        default="",
    )

    telefono_comprador = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    # -------------------------------------------------
    # COPIA DE LA DIRECCIÓN DEL PEDIDO
    # -------------------------------------------------
    # Guardamos estos datos directamente en el pedido
    # para que no dependan de que la dirección siga
    # existiendo o sea modificada posteriormente.

    nombre_direccion = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    calle = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    numero = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    comuna = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    region = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    informacion_adicional = models.TextField(
        blank=True,
        default="",
    )

    # -------------------------------------------------
    # ESTADO Y VALORES DEL PEDIDO
    # -------------------------------------------------

    estado = models.CharField(
        max_length=30,
        choices=ESTADOS,
        default="recibido",
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=0,
    )

    costo_despacho = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=2990,
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=0,
    )

    pago_confirmado = models.BooleanField(
        default=False,
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"Pedido #{self.id}"


class DetallePedido(models.Model):

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="detalles",
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="detalles_pedido",
    )

    nombre_producto = models.CharField(
        max_length=150,
    )

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=0,
    )

    cantidad = models.PositiveIntegerField()

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=0,
    )

    def __str__(self):
        return f"{self.nombre_producto} x {self.cantidad}"