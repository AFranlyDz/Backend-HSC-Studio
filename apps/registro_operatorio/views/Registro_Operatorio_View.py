from rest_framework import viewsets
from apps.registro_operatorio.models.Registro_Operatorio import (
    Registro_Operatorio,
)
from apps.registro_operatorio.serializers.Registro_Operatorio_Serial import (
    Registro_Operatorio_Serializer,
)


# Create your views here.
class Registro_Operatorio_View(viewsets.ModelViewSet):
    queryset = Registro_Operatorio.objects.all()
    serializer_class = Registro_Operatorio_Serializer
