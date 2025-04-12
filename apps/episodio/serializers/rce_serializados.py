from rest_framework import serializers
from ..models.rasgos_clinicos_episodio import Rasgos_Clinicos_Episodio


class rce_serializados(serializers.ModelSerializer):
    class Meta:
        model = Rasgos_Clinicos_Episodio
        fields = "__all__"


class rce_serializados_2(serializers.ModelSerializer):
    class Meta:
        model = Rasgos_Clinicos_Episodio
        fields = ["id", "codificador", "tiempo", "notas"]
        depth = 1
