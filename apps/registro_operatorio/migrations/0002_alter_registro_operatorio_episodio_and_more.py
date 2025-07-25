# Generated by Django 5.1.7 on 2025-04-20 01:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("episodio", "0002_initial"),
        ("registro_operatorio", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registro_operatorio",
            name="episodio",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="episodio_registro_operatorio",
                to="episodio.episodio",
            ),
        ),
        migrations.AlterField(
            model_name="registro_posoperatorio",
            name="registro_operatorio",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="registro_operatorio_posoperatorio",
                to="registro_operatorio.registro_operatorio",
            ),
        ),
    ]
