# Generated by Django 5.1.6 on 2025-03-24 21:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convocatorias', '0011_aprobacionacta'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='aprobacionacta',
            name='evaluador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='aprobacionacta',
            name='fecha_aprobacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
