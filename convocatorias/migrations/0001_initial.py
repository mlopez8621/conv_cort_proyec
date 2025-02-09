# Generated by Django 5.1.6 on 2025-02-10 14:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Postulacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo', models.TextField()),
                ('titulo', models.CharField(max_length=255)),
                ('anio_produccion', models.CharField(max_length=255)),
                ('duracion', models.TextField()),
                ('formato_grabacion', models.TextField()),
                ('productor_emp_produc', models.TextField()),
                ('nom_director', models.TextField()),
                ('sinopsis_corta', models.TextField()),
                ('locaciones_rodaje', models.TextField()),
                ('beneficiario_fdc', models.CharField(choices=[('si', 'Sí'), ('no', 'No')], default='no', max_length=2)),
                ('anio_fdc', models.PositiveIntegerField(blank=True, null=True)),
                ('certificacion_fdc', models.FileField(blank=True, null=True, upload_to='certificaciones/')),
                ('exhibicion_salas', models.CharField(choices=[('si', 'Sí'), ('no', 'No')], default='no', max_length=2)),
                ('plataformas_exhibicion', models.CharField(choices=[('si', 'Sí'), ('no', 'No'), ('otro', 'Otro')], default='no', max_length=10)),
                ('si_plataforma', models.CharField(blank=True, max_length=255, null=True)),
                ('resolucion_cpn', models.TextField()),
                ('fecha_resolucion_cpn', models.TextField()),
                ('certificacion_cpn', models.FileField(blank=True, null=True, upload_to='certificaciones/')),
                ('acta_clasificacion', models.FileField(blank=True, null=True, upload_to='certificaciones/')),
                ('tipo_persona', models.CharField(choices=[('natural', 'Persona Natural'), ('juridica', 'Persona Jurídica')], default='natural', max_length=10)),
                ('autorizacion_uso', models.FileField(blank=True, null=True, upload_to='autorizaciones/')),
                ('enlace_vimeo', models.URLField(help_text='Debe ser un enlace válido de Vimeo.', max_length=500, verbose_name='Enlace del corto en Vimeo')),
                ('contrasena_vimeo', models.CharField(blank=True, max_length=50, null=True, verbose_name='Contraseña del corto en Vimeo')),
                ('principales_festivales', models.TextField()),
                ('nombre_productor', models.TextField()),
                ('celular_productor', models.TextField()),
                ('domicilio_productor', models.TextField()),
                ('correo_productor', models.TextField()),
                ('postulado_antes', models.CharField(choices=[('si', 'Sí'), ('no', 'No')], default='no', max_length=2)),
                ('certificacion_cumplimiento', models.FileField(blank=True, null=True, upload_to='certificaciones/')),
                ('acepta_tyc', models.CharField(choices=[('si', 'Sí'), ('no', 'No')], default='no', max_length=2)),
                ('fecha_postulacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('evaluacion', 'En Evaluación'), ('rechazado', 'Rechazado'), ('aceptado', 'Aceptado')], default='pendiente', max_length=20)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentarios', models.TextField()),
                ('calificacion', models.IntegerField(default=0)),
                ('fecha_evaluacion', models.DateTimeField(auto_now_add=True)),
                ('evaluador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to=settings.AUTH_USER_MODEL)),
                ('postulacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convocatorias.postulacion')),
            ],
        ),
        migrations.CreateModel(
            name='Veredicto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision', models.CharField(choices=[('aprobado', 'Aprobado'), ('rechazado', 'Rechazado'), ('discusion', 'En Discusión')], max_length=20)),
                ('comentarios_finales', models.TextField()),
                ('fecha_veredicto', models.DateTimeField(auto_now_add=True)),
                ('postulacion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='convocatorias.postulacion')),
            ],
        ),
    ]
