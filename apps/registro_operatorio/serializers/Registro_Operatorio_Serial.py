from rest_framework import serializers
from apps.registro_operatorio.models.Registro_Operatorio import Registro_Operatorio
from apps.registro_operatorio.serializers.Registro_Posoperatorio_Serial import (
    Registro_Posoperatorio_Serial_Global,
)
from apps.registro_operatorio.serializers.Rasgos_Clinicos_Operatorios_Serial import (
    Rasgos_Clinicos_Operatorios_Serial_Global,
)


class Registro_Operatorio_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_Operatorio
        fields = "__all__"


class Registro_Operatorio_Serial_Global(serializers.ModelSerializer):
    registros_posoperatorios = Registro_Posoperatorio_Serial_Global(
        many=True, read_only=True, source="registro_operatorio_posoperatorio.all"
    )
    rasgos_clinicos_operatorios = Rasgos_Clinicos_Operatorios_Serial_Global(
        many=True, read_only=True, source="rasgos_clinicos_operatorios.all"
    )

    class Meta:
        model = Registro_Operatorio
        fields = [
            "id",
            "fecha_operacion",
            "es_reintervencion",
            "escala_evaluacion_resultados_glasgow",
            "estado_egreso",
            "observaciones",
            "registros_posoperatorios",
            "rasgos_clinicos_operatorios",
        ]
        depth = 1
