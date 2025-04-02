from rest_framework import serializers
from ..models.rasgos_clinicos_globales import Rasgos_Clinicos_Globales
from apps.codificadores.serializer import rc_serializados


class rcg_serializados(serializers.ModelSerializer):

    # codificador = rc_serializados(read_only=True)

    class Meta:
        model = Rasgos_Clinicos_Globales
        fields = ["id", "codificador", "notas"]
        depth = 1
