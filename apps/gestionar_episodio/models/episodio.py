from django.db import models
from apps.gestionar_historia_clinica.models.historia_clinica import historia_clinica


# Create your models here.
class Episodio(models.Model):
    historia_clinica = models.ForeignKey(
        historia_clinica,
        on_delete=models.CASCADE,
        related_name="historia_clinica_episodio",
    )
    inicio = models.DateField()
    fecha_alta = models.DateField()
    tiempo_estadia = models.IntegerField()
    estado_al_egreso = models.BooleanField()
    tiempo_antecedente = models.IntegerField()
    descripcion_antecedente = models.CharField(max_length=255)
    edad_paciente = models.IntegerField()
    observaciones = models.CharField(max_length=512, blank=True)

    class Meta:
        verbose_name = "episodio"
        verbose_name_plural = "episodios"
