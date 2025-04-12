from rest_framework import serializers
from apps.registro_operatorio.models.Registro_Posoperatorio import (
    Registro_Posoperatorio,
)


class Registro_Posoperatorio_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_Posoperatorio
        fields = "__all__"


class Registro_Posoperatorio_Serial_Global(serializers.ModelSerializer):
    class Meta:
        model = Registro_Posoperatorio
        fields = [
            "id",
            "fecha",
            "tiempo_transcurrido",
            "escala_pronostica_oslo_posoperatoria",
            "recurrencia_hematoma",
            "gradacion_pronostica_para_recurrencia_hsc_unilateral",
        ]
        depth = 1
