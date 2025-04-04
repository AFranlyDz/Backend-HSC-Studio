from rest_framework import serializers
from ..models.historia_clinica import historia_clinica
from apps.gestionar_historia_clinica.serializers.rcg_serializados import (
    rcg_serializados,
)
from apps.gestionar_episodio.serializers.episodio import episodio_serializado


class historia_clinica_serializada(serializers.ModelSerializer):
    rcg = rcg_serializados(many=True, source="historia_clinica.all")
    episodios = episodio_serializado(many=True, source="historia_clinica_episodio.all")

    class Meta:
        model = historia_clinica
        fields = [
            "id",
            "numero",
            "seudonimo",
            "nombre",
            "apellidos",
            "edad",
            "sexo",
            "historial_trauma_craneal",
            "manualidad",
            "antecedentes_familiares",
            "rcg",
            "episodios",
        ]
