from django.db import models


# Create your models here.
class historia_clinica(models.Model):
    numero = models.CharField(max_length=10)
    seudonimo = models.CharField(max_length=127)
    nombre = models.CharField(max_length=32)
    apellidos = models.CharField(max_length=63)
    edad = models.PositiveIntegerField()
    sexo = models.BooleanField()
    historial_trauma_craneal = models.BooleanField()
    manualidad = models.BooleanField()
    antecedentes_familiares = models.BooleanField()

    class Meta:
        verbose_name = "historia clínica"
        verbose_name_plural = "historias clínicas"
