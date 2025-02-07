from django import forms
from .models import Postulacion

class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ['titulo', 'descripcion', 'archivo_video']  # Excluir 'usuario' y 'estado'
