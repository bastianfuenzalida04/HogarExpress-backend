from django.urls import path

from .views import (
    CrearPedidoAPIView,
    MisPedidosAPIView,
    PedidoDetailAPIView,
    RepetirPedidoAPIView,
)


urlpatterns = [

    path(
        "crear/",
        CrearPedidoAPIView.as_view(),
        name="pedido-crear"
    ),

    path(
        "",
        MisPedidosAPIView.as_view(),
        name="mis-pedidos"
    ),

    path(
        "<int:pk>/",
        PedidoDetailAPIView.as_view(),
        name="pedido-detail"
    ),
    path(
    "<int:pk>/repetir/",
    RepetirPedidoAPIView.as_view(),
    name="pedido-repetir"
),
]