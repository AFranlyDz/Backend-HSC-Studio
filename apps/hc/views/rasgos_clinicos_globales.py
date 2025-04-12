from rest_framework import viewsets

from apps.hc.models.rasgos_clinicos_globales import (
    Rasgos_Clinicos_Globales,
)
from apps.hc.serializers.rcg_serializados import (
    rcg_serializados_2,
)


class rasgos_clinicos_globales_view(viewsets.ModelViewSet):
    queryset = Rasgos_Clinicos_Globales.objects.all()
    serializer_class = rcg_serializados_2
