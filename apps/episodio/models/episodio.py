from django.db import models
from apps.hc.models.historia_clinica import historia_clinica


# Create your models here.
class Episodio(models.Model):
    historia_clinica = models.ForeignKey(
        historia_clinica,
        on_delete=models.CASCADE,
        related_name="historia_clinica_episodio",
    )
    inicio = models.DateField(blank=True, null=True)
    fecha_alta = models.DateField(blank=True, null=True)
    tiempo_estadia = models.IntegerField(blank=True, null=True)
    estado_al_egreso = models.BooleanField()
    tiempo_antecedente = models.IntegerField(blank=True, null=True)
    descripcion_antecedente = models.CharField(max_length=255, blank=True, null=True)
    edad_paciente = models.IntegerField()
    observaciones = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        verbose_name = "episodio"
        verbose_name_plural = "episodios"
