from rest_framework import viewsets
from apps.registro_operatorio.models.Rasgos_Clinicos_Operatorios import (
    Rasgos_Clinicos_Operatorios,
)
from apps.registro_operatorio.serializers.Rasgos_Clinicos_Operatorios_Serial import (
    Rasgos_Clinicos_Operatorios_Serializer,
    Rasgos_Operatorios_Serializer_Read,
)
from django_filters.rest_framework import DjangoFilterBackend


class Rasgos_Clinicos_Operatorios_View(viewsets.ModelViewSet):
    """
    Viewset for the Rasgos Clinicos Operatorios model.
    """

    queryset = Rasgos_Clinicos_Operatorios.objects.all()
    serializer_class = Rasgos_Clinicos_Operatorios_Serializer


class Rasgos_Clinicos_Operatorios_Read(viewsets.ModelViewSet):
    queryset = Rasgos_Clinicos_Operatorios.objects.all()
    serializer_class = Rasgos_Operatorios_Serializer_Read
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["registro_operatorio__id"]
