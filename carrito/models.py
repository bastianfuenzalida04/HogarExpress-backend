from django.contrib.auth.models import User
from django.db import models

from productos.models import Producto


class Carrito(models.Model):

    # Usuario registrado.
    # Será NULL cuando el carrito pertenezca a un invitado.
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="carrito",
        null=True,
        blank=True,
    )

    # Identificador de sesión para usuarios invitados.
    session_key = models.CharField(
        max_length=40,
        unique=True,
        null=True,
        blank=True,
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        if self.usuario:
            return f"Carrito de {self.usuario.username}"

        return f"Carrito de invitado {self.session_key}"

    @property
    def total_items(self):
        return sum(
            item.cantidad
            for item in self.items.all()
        )

    @property
    def subtotal(self):
        return sum(
            item.subtotal
            for item in self.items.select_related(
                "producto"
            )
        )


class ItemCarrito(models.Model):

    carrito = models.ForeignKey(
        Carrito,
        on_delete=models.CASCADE,
        related_name="items"
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="items_carrito"
    )

    cantidad = models.PositiveIntegerField(
        default=1
    )

    fecha_agregado = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "carrito",
                    "producto"
                ],
                name="producto_unico_por_carrito"
            )
        ]

    def __str__(self):
        return (
            f"{self.producto.nombre} "
            f"x {self.cantidad}"
        )

    @property
    def subtotal(self):
        return (
            self.producto.precio *
            self.cantidad
        )