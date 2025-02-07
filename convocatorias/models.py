from django.db import models
from django.contrib.auth.models import User  # Usamos el modelo predeterminado de Django

class Postulacion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('evaluacion', 'En Evaluación'),
        ('rechazado', 'Rechazado'),
        ('aceptado', 'Aceptado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario que postula
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    archivo_video = models.FileField(upload_to='cortos/')  # Subida de archivos de video
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

