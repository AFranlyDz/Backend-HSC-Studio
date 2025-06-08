from django.db import models
from .historia_clinica import historia_clinica
from apps.codificadores.models import Codificadores


# Create your models here.
class Rasgos_Clinicos_Globales(models.Model):
    codificador = models.ForeignKey(
        Codificadores,
        on_delete=models.CASCADE,
        related_name="rasgos_globales",
        related_query_name="rasgo_global",
    )
    historia_clinica = models.ForeignKey(
        historia_clinica, on_delete=models.CASCADE, related_name="historia_clinica"
    )
    notas = models.CharField(max_length=512, blank=True)

    class Meta:
        verbose_name = "rasgo clinico global"
        verbose_name_plural = "rasgos clinicos globales"
