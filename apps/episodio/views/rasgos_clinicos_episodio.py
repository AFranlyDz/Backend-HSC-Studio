from rest_framework import viewsets

from apps.episodio.models.rasgos_clinicos_episodio import (
    Rasgos_Clinicos_Episodio,
)
from apps.episodio.serializers.rce_serializados import (
    rce_serializados,
)


class rasgo_clinico_episodio_view(viewsets.ModelViewSet):
    queryset = Rasgos_Clinicos_Episodio.objects.all()
    serializer_class = rce_serializados
