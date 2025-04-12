from rest_framework import viewsets
from ..models.historia_clinica import historia_clinica
from ..serializers.historia_clinica import historia_clinica_serializada
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class historia_clinica_listada(viewsets.ModelViewSet):
    queryset = historia_clinica.objects.all()
    serializer_class = historia_clinica_serializada
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
