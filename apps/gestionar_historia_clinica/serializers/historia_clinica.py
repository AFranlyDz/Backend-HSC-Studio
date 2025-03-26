from rest_framework import serializers
from ..models.historia_clinica import historia_clinica


class historia_clinica_serializada(serializers.ModelSerializer):
    class Meta:
        model = historia_clinica
        fields = "__all__"
