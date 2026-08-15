from django.urls import path

from .views import (
    CarritoAPIView,
    AgregarCarritoAPIView,
    ActualizarItemCarritoAPIView,
    EliminarItemCarritoAPIView,
    VaciarCarritoAPIView,
)


urlpatterns = [
    path(
        "",
        CarritoAPIView.as_view(),
        name="carrito"
    ),

    path(
        "agregar/",
        AgregarCarritoAPIView.as_view(),
        name="carrito-agregar"
    ),

    path(
        "item/<int:pk>/",
        ActualizarItemCarritoAPIView.as_view(),
        name="carrito-actualizar"
    ),

    path(
        "item/<int:pk>/eliminar/",
        EliminarItemCarritoAPIView.as_view(),
        name="carrito-eliminar"
    ),

    path(
        "vaciar/",
        VaciarCarritoAPIView.as_view(),
        name="carrito-vaciar"
    ),
]