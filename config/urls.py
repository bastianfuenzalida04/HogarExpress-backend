from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "api/usuarios/",
        include("usuarios.urls")
    ),

    path(
        "api/productos/",
        include("productos.urls")
    ),

    path(
        "api/carrito/",
        include("carrito.urls")
    ),

    path(
        "api/pedidos/",
        include("pedidos.urls")
    ),
]


# ============================================================
# ARCHIVOS MULTIMEDIA
# Permite mostrar las imágenes subidas desde el administrador
# durante el desarrollo
# ============================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )