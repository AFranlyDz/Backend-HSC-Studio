from django.db import models
from .Registro_Operatorio import Registro_Operatorio


class Registro_Posoperatorio(models.Model):
    registro_operatorio = models.ForeignKey(
        Registro_Operatorio,
        on_delete=models.CASCADE,
        related_name="registro_operatorio_posoperatorio",
    )
    fecha = models.DateField(blank=True, null=True)
    tiempo_transcurrido = models.IntegerField(blank=True, null=True)
    escala_pronostica_oslo_posoperatoria = models.IntegerField(blank=True, null=True)
    recurrencia_hematoma = models.BooleanField(blank=True, null=True)
    gradacion_pronostica_para_recurrencia_hsc_unilateral = models.IntegerField(
        blank=True, null=True
    )

    class Meta:
        verbose_name = "registro posoperatorio"
        verbose_name_plural = "registros posoperatorios"
