from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Direccion(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="direcciones"
    )

    nombre_direccion = models.CharField(
        max_length=100,
        default="Casa"
    )

    calle = models.CharField(max_length=150)
    numero = models.CharField(max_length=20)
    comuna = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    informacion_adicional = models.TextField(
        blank=True
    )

    principal = models.BooleanField(default=False)

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.comuna}"