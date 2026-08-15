from django.urls import path

from .views import (
    RegistroAPIView,
    LoginAPIView,
    LogoutAPIView,
    UsuarioActualAPIView,
    DireccionesAPIView,
    DireccionDetailAPIView,
    CSRFTokenAPIView,
)


urlpatterns = [
    path(
        "registro/",
        RegistroAPIView.as_view(),
        name="registro",
    ),

    path(
        "login/",
        LoginAPIView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="logout",
    ),

    path(
        "me/",
        UsuarioActualAPIView.as_view(),
        name="usuario-actual",
    ),

    path(
        "direcciones/",
        DireccionesAPIView.as_view(),
        name="direcciones",
    ),

    path(
        "direcciones/<int:pk>/",
        DireccionDetailAPIView.as_view(),
        name="direccion-detail",
    ),

    path(
        "csrf/",
        CSRFTokenAPIView.as_view(),
        name="csrf",
    ),
]