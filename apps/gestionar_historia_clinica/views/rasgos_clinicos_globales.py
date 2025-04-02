from rest_framework import viewsets

from apps.gestionar_historia_clinica.models.rasgos_clinicos_globales import (
    Rasgos_Clinicos_Globales,
)
from apps.gestionar_historia_clinica.serializers.rcg_serializados import (
    rcg_serializados,
)


class rasgos_clinicos_globales_view(viewsets.ModelViewSet):
    queryset = Rasgos_Clinicos_Globales.objects.all()
    serializer_class = rcg_serializados
