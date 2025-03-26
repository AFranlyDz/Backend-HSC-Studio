from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny

from ..models.rasgos_clinicos_globales import Rasgos_Clinicos_Globales
from ..serializers.rcg_serializados import rcg_serializados


@api_view(["GET", "POST", "DELETE", "PUT"])
@permission_classes([AllowAny])
def ver_rasgos_clinicos_globales(request, historia_clinica_id, codificador_id):
    if request.method == "GET":
        try:
            rasgos_clinicos_globales = Rasgos_Clinicos_Globales.objects.filter(
                historia_clinica_id=historia_clinica_id
            )
            serializador = rcg_serializados(rasgos_clinicos_globales, many=True)
            return Response(serializador.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    elif request.method == "POST":
        try:
            serializador = rcg_serializados(data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data, status=status.HTTP_201_CREATED)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    if request.method == "DELETE":
        try:
            rasgos_clinicos_globales = Rasgos_Clinicos_Globales.objects.filter(
                historia_clinica_id=historia_clinica_id
            ).filter(id=codificador_id)
            serializador = rcg_serializados(rasgos_clinicos_globales, many=True)
            rasgos_clinicos_globales.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Rasgos_Clinicos_Globales.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == "PUT":
        try:
            rasgos_clinicos_globales = Rasgos_Clinicos_Globales.objects.filter(
                historia_clinica_id=historia_clinica_id
            ).filter(id=codificador_id)
            serializador = rcg_serializados(
                rasgos_clinicos_globales, data=request.data, partial=True
            )
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data, status=status.HTTP_200_OK)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
