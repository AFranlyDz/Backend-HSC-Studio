from django.db import models


# Create your models here.
class Codificadores(models.Model):
    TRATAMIENTO_QUIRURGICO = "TRATAMIENTO_QUIRURGICO"
    CLASSIFICATION_CHOICES = [
        (TRATAMIENTO_QUIRURGICO, "Tratamiento quirúrgico"),
    ]
    nombre = models.CharField(max_length=255)
    nombre_corto = models.CharField(max_length=127, blank=True)
    descripcion = models.CharField(max_length=512, blank=True)
    clasificacion = models.CharField(max_length=255)

    class Meta:
        verbose_name = "codificador"
        verbose_name_plural = "codificadores"
