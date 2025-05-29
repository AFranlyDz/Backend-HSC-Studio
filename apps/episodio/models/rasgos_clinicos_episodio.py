from django.db import models
from .episodio import Episodio
from apps.codificadores.models import Codificadores


# Create your models here.
class Rasgos_Clinicos_Episodio(models.Model):
    codificador = models.ForeignKey(
        Codificadores,
        on_delete=models.CASCADE,
        related_name="rasgos_episodios",
        related_query_name="rasgo_episodio",
    )
    episodio = models.ForeignKey(
        Episodio, on_delete=models.CASCADE, related_name="episodio_rce"
    )
    tiempo = models.IntegerField(blank=True, null=True)
    notas = models.CharField(max_length=512)

    class Meta:
        verbose_name = "rasgo clinico del episodio"
        verbose_name_plural = "resgos clinicos del episodio"
