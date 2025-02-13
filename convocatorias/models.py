from django.db import models
from django.contrib.auth.models import User  # Usamos el modelo predeterminado de Django
from django.core.validators import RegexValidator

class Postulacion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('evaluacion', 'En Evaluación'),
        ('rechazado', 'Rechazado'),
        ('aceptado', 'Aceptado'),
    ]

    BENEFICIARIO_CHOICES = [
        ('si', 'Sí'),
        ('no', 'No'),
    ]

    EXHIBICION_CHOICES = [
        ('si', 'Sí'),
        ('no', 'No'),
    ]

    PLATAFORMAS_CHOICES = [
        ('si', 'Sí'),
        ('no', 'No'),
        ('otro', 'Otro'),
    ]

    POSTULADO_ANTES_CHOICES = [
        ('si', 'Sí'),
        ('no', 'No'),
    ]

    ACEPTA_TYC_CHOICES= [
        ('si', 'Sí'),
        ('no', 'No'),
    ]

    TIPO_PERSONA_CHOICES = [
        ('natural', 'Persona Natural'),
        ('juridica', 'Persona Jurídica'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario que postula
    correo = models.EmailField(unique=True, max_length=255)
    titulo = models.CharField(max_length=255)
    anio_produccion = models.IntegerField(verbose_name="Año de producción")
    duracion = models.TimeField(verbose_name="Duración (Min)", help_text="Formato HH:MM")
    formato_grabacion = models.CharField(max_length=255)
    productor_emp_produc = models.CharField(max_length=255,verbose_name="Productor o empresa productora")
    nom_director = models.CharField(max_length=255,verbose_name="Nombre del director")
    sinopsis_corta = models.TextField(verbose_name="Storyline / Sinopsis Corta")
    locaciones_rodaje = models.TextField()
    beneficiario_fdc = models.CharField(max_length=2, choices=BENEFICIARIO_CHOICES, default='no',verbose_name="El corto ha sido beneficiario de la convocatoria del FDC para cortos")
    anio_fdc = models.PositiveIntegerField(null=True, blank=True,verbose_name="Año del beneficio")
    certificacion_fdc = models.FileField(upload_to='certificaciones/', null=True, blank=True,verbose_name="Certificado del beneficio FDC")
    exhibicion_salas = models.CharField(max_length=2,choices=EXHIBICION_CHOICES,default='no')
    plataformas_exhibicion = models.CharField(max_length=10, choices=PLATAFORMAS_CHOICES,default='no')
    si_plataforma = models.CharField(max_length=255, blank=True, null=True,verbose_name="¿Cuales plataformas?")
    resolucion_cpn = models.PositiveIntegerField(null=True, blank=True)
    fecha_resolucion_cpn = models.DateField(null=True, blank=True)
    certificacion_cpn = models.FileField(upload_to='certificaciones/', null=True, blank=True)
    acta_clasificacion = models.FileField(upload_to='certificaciones/', null=True, blank=True)
    tipo_persona = models.CharField(max_length=10, choices=TIPO_PERSONA_CHOICES,default='natural')
    autorizacion_uso = models.FileField(upload_to='autorizaciones/', null=True, blank=True)
    enlace_vimeo = models.URLField(max_length=500, verbose_name="Enlace del corto en Vimeo", blank=True, null=True)
    contrasena_vimeo = models.CharField(max_length=50, verbose_name="Contraseña del corto en Vimeo", blank=True, null=True)
    principales_festivales = models.TextField()
    nombre_productor = models.CharField(max_length=255)
    celular_productor = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\+?\d{1,15}$',            message="Número inválido. Use el formato: +573001234567 o 3001234567")],verbose_name="Número de celular del productor")
    domicilio_productor = models.CharField(max_length=255)
    correo_productor = models.EmailField(unique=True, max_length=255)
    postulado_antes = models.CharField(max_length=2, choices=POSTULADO_ANTES_CHOICES, default='no')
    certificacion_cumplimiento = models.FileField(upload_to='certificaciones/', null=True, blank=True)
    acepta_tyc = models.CharField(max_length=2, choices=ACEPTA_TYC_CHOICES, default='no')
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"


class Evaluacion(models.Model):
    postulacion = models.ForeignKey(Postulacion, on_delete=models.CASCADE)
    evaluador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluaciones')  # Evaluador es un usuario
    comentarios = models.TextField()
    calificacion = models.IntegerField(default=0)  # Nota del evaluador (escala 1-10 por ejemplo)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluación de {self.postulacion.titulo} por {self.evaluador.username}"


class Veredicto(models.Model):
    DECISION_CHOICES = [
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('discusion', 'En Discusión'),
    ]

    postulacion = models.OneToOneField(Postulacion, on_delete=models.CASCADE)
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES)
    comentarios_finales = models.TextField()
    fecha_veredicto = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Veredicto para {self.postulacion.titulo}: {self.decision}"

