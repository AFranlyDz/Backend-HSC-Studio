from rest_framework import serializers
from ..models.episodio import Episodio
from apps.episodio.serializers.rce_serializados import rce_serializados_2
from apps.registro_operatorio.serializers.Registro_Operatorio_Serial import (
    Registro_Operatorio_Serial_Global,
)
from apps.hematoma.serializers import Hematoma_Subdural_Serial_Global


class episodio_serializado(serializers.ModelSerializer):
    rce = rce_serializados_2(many=True, read_only=True, source="episodio_rce.all")
    registro_operatorio = Registro_Operatorio_Serial_Global(
        many=True, read_only=True, source="episodio_registro_operatorio.all"
    )
    hematomas_subdurales = Hematoma_Subdural_Serial_Global(
        many=True, read_only=True, source="hematoma_episodio.all"
    )

    class Meta:
        model = Episodio
        fields = [
            "id",
            "inicio",
            "fecha_alta",
            "tiempo_estadia",
            "estado_al_egreso",
            "tiempo_antecedente",
            "descripcion_antecedente",
            "edad_paciente",
            "observaciones",
            "rce",
            "registro_operatorio",
            "hematomas_subdurales",
        ]


class episodio_serializado_2(serializers.ModelSerializer):
    class Meta:
        model = Episodio
        fields = "__all__"
