from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models.episodio import Episodio
from ..serializers.episodio import episodio_serializado


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def episodios_por_historia_clinica(request, historia_clinica_id):
    if request.method == "GET":
        try:
            episodios = Episodio.objects.filter(historia_clinica_id=historia_clinica_id)
            serializador = episodio_serializado(episodios, many=True)
            return Response(serializador.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    elif request.method == "POST":
        try:
            # Agregar el ID de la historia clínica al request data
            request.data["historia_clinica_id"] = historia_clinica_id
            serializador = episodio_serializado(data=request.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data, status=status.HTTP_201_CREATED)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


@api_view(["GET", "DELETE", "PUT"])
@permission_classes([AllowAny])
def ver_episodio(request, historia_clinica_id, episodio_id):
    if request.method == "GET":
        try:
            episodios = Episodio.objects.filter(
                historia_clinica_id=historia_clinica_id, id=episodio_id
            )
            serializador = episodio_serializado(episodios, many=True)
            return Response(serializador.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    if request.method == "DELETE":
        try:
            episodios = Episodio.objects.filter(
                historia_clinica_id=historia_clinica_id
            ).filter(id=episodio_id)
            serializador = episodio_serializado(episodios, many=True)
            episodios.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Episodio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "PUT":
        try:
            episodio = Episodio.objects.get(id=episodio_id)
            serializador = episodio_serializado(
                episodio, data=request.data, partial=True
            )
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data, status=status.HTTP_200_OK)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
