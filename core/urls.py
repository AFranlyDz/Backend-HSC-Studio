"""
URL configuration for HSCStudio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import DefaultRouter

from apps.gestionar_historia_clinica.views.historia_clinica import (
    historia_clinica_listada,
)
from apps.gestionar_historia_clinica.views.rasgos_clinicos_globales import (
    ver_rasgos_clinicos_globales,
)
from apps.gestionar_episodio.views.episodio import (
    episodios_por_historia_clinica,
    ver_episodio,
)
from apps.gestionar_episodio.views.rasgos_clinicos_episodio import (
    ver_rasgos_clinicos_episodio,
)
from apps.codificadores.views import ver_codificadores

router = DefaultRouter()
router.register(r"gestionar_historia_clinica", historia_clinica_listada)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/", include(router.urls), name="historia_clinica_listada"),
    path(
        "api/gestionar_episodios/<int:historia_clinica_id>/",
        episodios_por_historia_clinica,
        name="obtener_episodios_por_id",
    ),
    path(
        "api/gestionar_episodios/<int:historia_clinica_id>/<int:episodio_id>/",
        ver_episodio,
        name="episodio",
    ),
    path(
        "api/gestionar_codificadores/<int:codigo>/",
        ver_codificadores,
        name="Codificadores",
    ),
    path(
        "api/gestionar_rasgos_clinicos_globales/<int:historia_clinica_id>/<int:codificador_id>/",
        ver_rasgos_clinicos_globales,
        name="Rasgos Clinicos Globales",
    ),
    path(
        "api/gestionar_rasgos_clinicos_episodio/<int:episodio_id>/<int:codificador_id>/",
        ver_rasgos_clinicos_episodio,
        name="Rasgos Clinicos del Episodio",
    ),
]
