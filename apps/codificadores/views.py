from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Codificadores
from .serializer import rc_serializados


@api_view(["GET"])
@permission_classes([AllowAny])
def ver_codificadores(request, codigo):
    if codigo == 1:
        try:
            valores_filtro = [
                "Factor de Riesgo",
                "Antecedente Neurologico",
                "Antecedente Patologico Personal",
                "Factor Predisponente",
                "Lesion Isquemica Asociada",
            ]
            rasgos_clinicos = Codificadores.objects.filter(
                clasificacion__in=valores_filtro
            )
            serializador = rc_serializados(rasgos_clinicos, many=True)
            return Response(serializador.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    elif codigo == 2:
        try:
            valores_filtro = ["Sintoma", "Forma Clinica de Presentacion"]
            rasgos_clinicos = Codificadores.objects.filter(
                clasificacion__in=valores_filtro
            )
            serializador = rc_serializados(rasgos_clinicos, many=True)
            return Response(serializador.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
