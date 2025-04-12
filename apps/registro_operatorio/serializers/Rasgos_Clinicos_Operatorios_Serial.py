from rest_framework import serializers
from apps.registro_operatorio.models.Rasgos_Clinicos_Operatorios import (
    Rasgos_Clinicos_Operatorios,
)


class Rasgos_Clinicos_Operatorios_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Rasgos_Clinicos_Operatorios
        fields = "__all__"


class Rasgos_Clinicos_Operatorios_Serial_Global(serializers.ModelSerializer):
    class Meta:
        model = Rasgos_Clinicos_Operatorios
        fields = (
            "id",
            "codificador",
        )
        depth = 1
