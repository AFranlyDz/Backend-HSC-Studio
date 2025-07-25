from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.episodio.models.episodio import Episodio


# Create your models here.
class hematoma_subdural(models.Model):
    episodio = models.ForeignKey(
        Episodio, on_delete=models.CASCADE, related_name="hematoma_episodio"
    )
    escala_glasgow_ingreso = models.IntegerField(
        validators=[MinValueValidator(3), MaxValueValidator(15)],
    )
    escala_mcwalder = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    escala_gordon_firing = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    escala_pronostica_oslo_preoperatoria = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    escala_nomura = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    escala_nakagushi = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    valor_longitud = models.IntegerField()
    valor_diametro = models.IntegerField()
    valor_altura = models.IntegerField()
    volumen_tada = models.IntegerField()
    volumen = models.IntegerField()
    grupo_volumen = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    grupo_volumen_residual_posoperatorio = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    diametro_capa = models.IntegerField()
    diametro_mayor_transverso = models.IntegerField()
    grupo_diametro = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    presencia_membrana = models.BooleanField()
    tipo_membrana = models.IntegerField()
    localización = models.CharField(max_length=255)
    topografia = models.CharField(max_length=255)
    desviacion_linea_media = models.IntegerField()
    metodo_lectura = models.BooleanField()
    observaciones = models.CharField(max_length=512)

    class Meta:
        verbose_name = "hematoma subdural"
        verbose_name_plural = "hematomas subdurales"
