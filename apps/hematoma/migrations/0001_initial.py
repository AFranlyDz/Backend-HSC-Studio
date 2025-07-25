# Generated by Django 5.1.7 on 2025-04-20 01:29

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("episodio", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="hematoma_subdural",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "escala_glasgow_ingreso",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(3),
                            django.core.validators.MaxValueValidator(15),
                        ]
                    ),
                ),
                (
                    "escala_mcwalder",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(4),
                        ]
                    ),
                ),
                (
                    "escala_gordon_firing",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(4),
                        ]
                    ),
                ),
                (
                    "escala_pronostica_oslo_preoperatoria",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                (
                    "escala_nomura",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                (
                    "escala_nakagushi",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(4),
                        ]
                    ),
                ),
                ("valor_longitud", models.IntegerField()),
                ("valor_diametro", models.IntegerField()),
                ("valor_altura", models.IntegerField()),
                ("volumen_tada", models.IntegerField()),
                ("volumen", models.IntegerField()),
                (
                    "grupo_volumen",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(4),
                        ]
                    ),
                ),
                (
                    "grupo_volumen_residual_posoperatorio",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(4),
                        ]
                    ),
                ),
                ("diametro_capa", models.IntegerField()),
                ("diametro_mayor_transverso", models.IntegerField()),
                (
                    "grupo_diametro",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(4),
                        ]
                    ),
                ),
                ("presencia_membrana", models.BooleanField()),
                ("tipo_membrana", models.IntegerField()),
                ("localización", models.CharField(max_length=255)),
                ("topografia", models.CharField(max_length=255)),
                ("desviacion_linea_media", models.IntegerField()),
                ("metodo_lectura", models.BooleanField()),
                ("observaciones", models.CharField(max_length=512)),
                (
                    "episodio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hematoma_episodio",
                        to="episodio.episodio",
                    ),
                ),
            ],
            options={
                "verbose_name": "hematoma subdural",
                "verbose_name_plural": "hematomas subdurales",
            },
        ),
    ]
