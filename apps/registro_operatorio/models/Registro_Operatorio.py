from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.episodio.models.episodio import Episodio


# Create your models here.
class Registro_Operatorio(models.Model):
    episodio = models.ForeignKey(
        Episodio, on_delete=models.CASCADE, related_name="episodio_registro_operatorio"
    )
    fecha_operacion = models.DateField(blank=True, null=True)
    es_reintervencion = models.BooleanField()
    escala_evaluacion_resultados_glasgow = models.IntegerField(
        validators=[MinValueValidator(3), MaxValueValidator(15)],
    )
    estado_egreso = models.BooleanField()
    observaciones = models.CharField(max_length=512, blank=True)

    class Meta:
        verbose_name = "registro operatorio"
        verbose_name = "registros operatorios"
