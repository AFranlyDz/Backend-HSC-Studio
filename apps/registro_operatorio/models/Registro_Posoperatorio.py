from django.db import models
from .Registro_Operatorio import Registro_Operatorio


class Registro_Posoperatorio(models.Model):
    registro_operatorio = models.ForeignKey(
        Registro_Operatorio,
        on_delete=models.CASCADE,
        related_name="registro_operatorio_posoperatorio",
    )
    fecha = models.DateField()
    tiempo_transcurrido = models.IntegerField()
    escala_pronostica_oslo_posoperatoria = models.IntegerField()
    recurrencia_hematoma = models.BooleanField()
    gradacion_pronostica_para_recurrencia_hsc_unilateral = models.IntegerField()

    class Meta:
        verbose_name = "registro posoperatorio"
        verbose_name_plural = "registros posoperatorios"
