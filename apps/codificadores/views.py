from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Codificadores
from .serializer import rc_serializados


class Codificadores_View(viewsets.ModelViewSet):
    queryset = Codificadores.objects.all()
    serializer_class = rc_serializados
