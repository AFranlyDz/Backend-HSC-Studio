from django.db import models


# Create your models here.
class Codificadores(models.Model):
    nombre = models.CharField(max_length=255)
    nombre_corto = models.CharField(max_length=127)
    descripcion = models.CharField(max_length=512)
    clasificacion = models.CharField(max_length=255)

    class Meta:
        verbose_name = "codificador"
        verbose_name_plural = "codificadores"
