from rest_framework import viewsets
from apps.hematoma.models import hematoma_subdural
from apps.hematoma.serializers import Hematoma_Subdural_Serializer


# Create your views here.
class Hematoma_Subdural_View(viewsets.ModelViewSet):
    queryset = hematoma_subdural.objects.all()
    serializer_class = Hematoma_Subdural_Serializer
