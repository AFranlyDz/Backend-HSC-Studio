from rest_framework import viewsets

from apps.gestionar_episodio.models.episodio import (
    Episodio,
)
from apps.gestionar_episodio.serializers.episodio import (
    episodio_serializado_2,
)


class episodio_view(viewsets.ModelViewSet):
    queryset = Episodio.objects.all()
    serializer_class = episodio_serializado_2
