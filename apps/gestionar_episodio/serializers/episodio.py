from rest_framework import serializers
from ..models.episodio import Episodio


class episodio_serializado(serializers.ModelSerializer):
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
        ]


class episodio_serializado_2(serializers.ModelSerializer):
    class Meta:
        model = Episodio
        fields = "__all__"
