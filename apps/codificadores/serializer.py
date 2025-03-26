from rest_framework import serializers
from .models import Codificadores


class rc_serializados(serializers.ModelSerializer):
    class Meta:
        model = Codificadores
        fields = "__all__"
