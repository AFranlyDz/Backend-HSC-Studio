from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny

from ..models.rasgos_clinicos_episodio import Rasgos_Clinicos_Episodio
from ..serializers.rce_serializados import rce_serializados


@api_view(["GET", "POST", "DELETE", "PUT"])
@permission_classes([AllowAny])
def ver_rasgos_clinicos_episodio(request, episodio_id, codificador_id):
    if request.method == "GET":
        try:
            rasgos_clinicos_episodio = Rasgos_Clinicos_Episodio.objects.filter(
                episodio_id=episodio_id
            )
            serializador = rce_serializados(rasgos_clinicos_episodio, many=True)
            return Response(serializador.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    elif request.method == "POST":
        try:
            serializador = rce_serializados(data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data, status=status.HTTP_201_CREATED)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    if request.method == "DELETE":
        try:
            rasgos_clinicos_episodio = Rasgos_Clinicos_Episodio.objects.filter(
                episodio_id=episodio_id
            ).filter(id=codificador_id)
            serializador = rce_serializados(rasgos_clinicos_episodio, many=True)
            rasgos_clinicos_episodio.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Rasgos_Clinicos_Episodio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == "PUT":
        try:
            rasgos_clinicos_episodio = Rasgos_Clinicos_Episodio.objects.filter(
                episodio_id=episodio_id
            ).filter(id=codificador_id)
            serializador = rce_serializados(
                rasgos_clinicos_episodio, data=request.data, partial=True
            )
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data, status=status.HTTP_200_OK)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
