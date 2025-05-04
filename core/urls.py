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

from apps.hc.views.historia_clinica import (
    historia_clinica_listada,
)
from apps.hc.views.rasgos_clinicos_globales import (
    rasgos_clinicos_globales_view,
)
from apps.episodio.views.episodio import episodio_view
from apps.episodio.views.rasgos_clinicos_episodio import (
    rasgo_clinico_episodio_view,
)
from apps.codificadores.views import Codificadores_View
from apps.registro_operatorio.views.Registro_Operatorio_View import (
    Registro_Operatorio_View,
)
from apps.registro_operatorio.views.Registro_Posoperatorio_View import (
    Registro_Posoperatorio_View,
)
from apps.registro_operatorio.views.Rasgos_Clinicos_Operatorios_View import (
    Rasgos_Clinicos_Operatorios_View,
)
from apps.hematoma.views import Hematoma_Subdural_View
from apps.exportar_csv.views import ExportCSVView

router = DefaultRouter()
router.register(
    r"gestionar_historia_clinica",
    historia_clinica_listada,
    basename="historias-clinicas",
)
router.register(
    r"rasgos_clinicos_globales",
    rasgos_clinicos_globales_view,
    basename="rasgos-clinicos-globales",
)
router.register(r"codificadores", Codificadores_View, basename="codificadores")
router.register(r"episodios", episodio_view, basename="episodios")
router.register(
    r"rasgos_clinicos_episodio",
    rasgo_clinico_episodio_view,
    basename="rasgos-clinicos-episodio",
)
router.register(
    r"registro_operatorio", Registro_Operatorio_View, basename="registro-operatorio"
)
router.register(
    r"registro_posoperatorio",
    Registro_Posoperatorio_View,
    basename="registro-posoperatorio",
)
router.register(
    r"rasgos_clinicos_operatorios",
    Rasgos_Clinicos_Operatorios_View,
    basename="rasgos-clinicos-operatorios",
)
router.register(
    r"hematomas_subdurales", Hematoma_Subdural_View, basename="hematomas-subdurales"
)
### router.register(r"export-csv", ExportCSVView.as_view(), basename="export-csv")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/", include(router.urls)),
    path("api/export-csv/", ExportCSVView.as_view(), name="export-csv"),
]
