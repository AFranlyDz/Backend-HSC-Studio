from rest_framework import serializers
from ..models.rasgos_clinicos_globales import Rasgos_Clinicos_Globales


class rcg_serializados(serializers.ModelSerializer):
    class Meta:
        model = Rasgos_Clinicos_Globales
        fields = "__all__"
