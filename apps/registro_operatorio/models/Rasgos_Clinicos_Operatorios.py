from django.db import models
from .Registro_Operatorio import Registro_Operatorio
from apps.codificadores.models import Codificadores


class Rasgos_Clinicos_Operatorios(models.Model):
    registro_operatorio = models.ForeignKey(
        Registro_Operatorio,
        on_delete=models.CASCADE,
        related_name="rasgos_clinicos_operatorios",
    )
    codificador = models.ForeignKey(
        Codificadores, on_delete=models.CASCADE, related_name="codificador_operatorio"
    )

    class Meta:
        verbose_name = "rasgo clinico operatorio"
        verbose_name_plural = "rasgos clinicos operatorios"
