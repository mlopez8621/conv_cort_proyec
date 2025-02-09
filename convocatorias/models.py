from django.db import models
from django.contrib.auth.models import User  # Usamos el modelo predeterminado de Django

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

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario que postula
    correo = models.TextField()
    titulo = models.CharField(max_length=255)
    anio_produccion = models.CharField(max_length=255)
    duracion = models.TextField()
    formato_grabacion = models.TextField()
    productor_emp_produc = models.TextField()
    nom_director = models.TextField()
    sinopsis_corta = models.TextField()
    locaciones_rodaje = models.TextField()
    beneficiario_fdc = models.CharField(max_length=2, choices=BENEFICIARIO_CHOICES, default='no')
    anio_fdc = models.PositiveIntegerField(null=True, blank=True)
    certificacion_fdc = models.FileField(upload_to='certificaciones/', null=True, blank=True)
    exhibicion_salas = models.CharField(max_length=2,choices=EXHIBICION_CHOICES,default='no')
    plataformas_exhibicion = models.CharField(max_length=10, choices=PLATAFORMAS_CHOICES,default='no')
    si_plataforma = models.CharField(max_length=255, blank=True, null=True)
    resolucion_cpn = models.TextField() 
    fecha_resolucion_cpn = models.TextField() 
    certificacion_cpn = models.FileField(upload_to='certificaciones/', null=True, blank=True)
    acta_clasificacion = models.FileField(upload_to='certificaciones/', null=True, blank=True)
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

