from rest_framework import serializers
from apps.hematoma.models import hematoma_subdural


class Hematoma_Subdural_Serializer(serializers.ModelSerializer):
    class Meta:
        model = hematoma_subdural
        fields = "__all__"


class Hematoma_Subdural_Serial_Global(serializers.ModelSerializer):
    class Meta:
        model = hematoma_subdural
        fields = [
            "id",
            "escala_glasgow_ingreso",
            "escala_mcwalder",
            "escala_gordon_firing",
            "escala_pronostica_oslo_preoperatoria",
            "escala_nomura",
            "escala_nakagushi",
            "valor_longitud",
            "valor_diametro",
            "valor_altura",
            "volumen_tada",
            "volumen",
            "grupo_volumen",
            "grupo_volumen_residual_posoperatorio",
            "diametro_capa",
            "diametro_mayor_transverso",
            "grupo_diametro",
            "presencia_membrana",
            "tipo_membrana",
            "localización",
            "topografia",
            "desviacion_linea_media",
            "metodo_lectura",
            "observaciones",
        ]
        depth = 1
