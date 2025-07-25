# Generated by Django 5.1.7 on 2025-03-26 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Codificadores",
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
                ("nombre", models.CharField(max_length=255)),
                ("nombre_corto", models.CharField(max_length=127)),
                ("descripcion", models.CharField(max_length=512)),
                ("clasificacion", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "Codificador",
                "verbose_name_plural": "Codificadores",
            },
        ),
    ]
