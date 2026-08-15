from django.db.models import Q

from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Categoria, Producto
from .serializers import (
    CategoriaSerializer,
    ProductoSerializer,
)


def quitar_acentos(texto):
    """
    Normaliza un texto eliminando acentos y convirtiéndolo
    a minúsculas para facilitar las búsquedas.
    """
    import unicodedata

    texto = texto or ""

    return "".join(
        caracter
        for caracter in unicodedata.normalize(
            "NFD",
            texto
        )
        if unicodedata.category(caracter) != "Mn"
    ).lower()


class CategoriaListAPIView(generics.ListAPIView):
    queryset = Categoria.objects.filter(activa=True)
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]


class CategoriaDetailAPIView(generics.RetrieveAPIView):
    queryset = Categoria.objects.filter(activa=True)
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]


class ProductoListAPIView(generics.ListAPIView):
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Producto.objects.filter(
            activo=True
        ).select_related("categoria")

        categoria = self.request.query_params.get(
            "categoria"
        )

        buscar = self.request.query_params.get(
            "buscar"
        )

        destacado = self.request.query_params.get(
            "destacado"
        )

        # =====================================================
        # FILTRO POR CATEGORÍA
        # =====================================================

        if categoria:
            queryset = queryset.filter(
                categoria_id=categoria
            )

        # =====================================================
        # BÚSQUEDA
        # =====================================================

        if buscar:
            buscar_normalizado = quitar_acentos(
                buscar
            )

            productos_filtrados = []

            for producto in queryset:
                nombre = quitar_acentos(
                    producto.nombre
                )

                descripcion = quitar_acentos(
                    producto.descripcion
                )

                if (
                    buscar_normalizado in nombre
                    or buscar_normalizado in descripcion
                ):
                    productos_filtrados.append(
                        producto.pk
                    )

            queryset = queryset.filter(
                pk__in=productos_filtrados
            )

        # =====================================================
        # DESTACADOS
        # =====================================================

        if destacado == "true":
            queryset = queryset.filter(
                destacado=True
            )

        return queryset


class ProductoDetailAPIView(generics.RetrieveAPIView):
    queryset = Producto.objects.filter(
        activo=True
    ).select_related("categoria")

    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]