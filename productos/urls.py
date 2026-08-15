from django.urls import path

from .views import (
    CategoriaListAPIView,
    CategoriaDetailAPIView,
    ProductoListAPIView,
    ProductoDetailAPIView,
)


urlpatterns = [
    path(
        "categorias/",
        CategoriaListAPIView.as_view(),
        name="categorias",
    ),

    path(
        "categorias/<int:pk>/",
        CategoriaDetailAPIView.as_view(),
        name="categoria-detail",
    ),

    path(
        "",
        ProductoListAPIView.as_view(),
        name="productos",
    ),

    path(
        "<int:pk>/",
        ProductoDetailAPIView.as_view(),
        name="producto-detail",
    ),
]