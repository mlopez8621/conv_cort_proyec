# Generated by Django 5.1.6 on 2025-03-24 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convocatorias', '0008_actaevaluacion_postulacion_acta'),
    ]

    operations = [
        migrations.AddField(
            model_name='postulacion',
            name='comentario_final',
            field=models.TextField(blank=True, null=True, verbose_name='Comentario final del acta'),
        ),
    ]
