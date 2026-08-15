from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Perfil, Direccion


class RegistroSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    nombre = serializers.CharField(max_length=100)
    apellido = serializers.CharField(max_length=100)
    telefono = serializers.CharField(max_length=20, required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Este nombre de usuario ya está registrado."
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Este correo electrónico ya está registrado."
            )
        return value

    def create(self, validated_data):
        nombre = validated_data.pop("nombre")
        apellido = validated_data.pop("apellido")
        telefono = validated_data.pop("telefono", "")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        Perfil.objects.create(
            usuario=user,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
        )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source="perfil.nombre", read_only=True)
    apellido = serializers.CharField(source="perfil.apellido", read_only=True)
    telefono = serializers.CharField(source="perfil.telefono", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "nombre",
            "apellido",
            "telefono",
        ]


class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = [
            "id",
            "nombre_direccion",
            "calle",
            "numero",
            "comuna",
            "region",
            "informacion_adicional",
            "principal",
        ]
        read_only_fields = ["id"]