# Generated by Django 5.1.6 on 2025-03-29 22:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convocatorias', '0013_alter_actaevaluacion_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aprobacionacta',
            name='evaluador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convocatorias.evaluador'),
        ),
        migrations.CreateModel(
            name='BancoCortos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_agregado', models.DateTimeField(auto_now_add=True)),
                ('postulacion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='banco', to='convocatorias.postulacion')),
            ],
            options={
                'verbose_name': 'Cortometraje en el Banco',
                'verbose_name_plural': 'Banco de Cortos',
            },
        ),
    ]
