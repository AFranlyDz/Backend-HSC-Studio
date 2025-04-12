from rest_framework import viewsets
from apps.registro_operatorio.models.Registro_Posoperatorio import (
    Registro_Posoperatorio,
)
from apps.registro_operatorio.serializers.Registro_Posoperatorio_Serial import (
    Registro_Posoperatorio_Serializer,
)


class Registro_Posoperatorio_View(viewsets.ModelViewSet):
    queryset = Registro_Posoperatorio.objects.all()
    serializer_class = Registro_Posoperatorio_Serializer
