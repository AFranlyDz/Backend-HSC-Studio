from rest_framework import viewsets
from apps.registro_operatorio.models.Rasgos_Clinicos_Operatorios import (
    Rasgos_Clinicos_Operatorios,
)
from apps.registro_operatorio.serializers.Rasgos_Clinicos_Operatorios_Serial import (
    Rasgos_Clinicos_Operatorios_Serializer,
)


class Rasgos_Clinicos_Operatorios_View(viewsets.ModelViewSet):
    """
    Viewset for the Rasgos Clinicos Operatorios model.
    """

    queryset = Rasgos_Clinicos_Operatorios.objects.all()
    serializer_class = Rasgos_Clinicos_Operatorios_Serializer
