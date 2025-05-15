from django import forms
from .models import Postulacion
from .models import Evaluacion
from datetime import time
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re

class PostulacionForm(forms.ModelForm):

    duracion = forms.CharField(
        label="Duración (MM:SS)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ejemplo: 08:30',
            'required': 'required'
        })
    )

    def clean_duracion(self):
        data = self.cleaned_data['duracion']
        try:
            minutos, segundos = map(int, data.split(':'))
            return timedelta(minutes=minutos, seconds=segundos)
        except:
            raise forms.ValidationError("La duración debe estar en formato MM:SS")
        
    class Meta:
        model = Postulacion
        fields = ['titulo', 'anio_produccion','duracion','genero_cortrometraje','subgenero_cortrometraje',
                  'otro_subgenero_cortrometraje','formato_grabacion','productor_emp_produc',
                  'nom_director','sinopsis_corta','locaciones_rodaje','beneficiario_fdc', 'anio_fdc',
                  'certificacion_fdc','exhibicion_salas','plataformas_exhibicion', 'si_plataforma','resolucion_cpn',
                  'fecha_resolucion_cpn','certificacion_cpn', 'acta_clasificacion','tipo_persona','autorizacion_uso',
                  'enlace_vimeo','contrasena_vimeo','principales_festivales','nombre_productor','celular_productor',
                  'domicilio_productor','correo_productor','postulado_antes','certificacion_cumplimiento','acepta_tyc',
                 ]  # Excluir 'usuario' y 'estado'

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_titulo','placeholder': 'Ingrese el titulo','required': 'required'}),
            'anio_produccion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese año de produccion','required': 'required'}),
            'genero_cortrometraje': forms.RadioSelect(attrs={'class': 'form-check-input', 'id': 'id_genero_cortrometraje','required': 'required'}),
            'subgenero_cortrometraje': forms.RadioSelect(attrs={'class': 'form-check-input', 'id': 'id_subgenero_cortrometraje','required': 'required'}),
            'otro_subgenero_cortrometraje': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_otro_subgenero_cortrometraje','placeholder': 'Ingrese otro subgenero','required': 'required'}),
            'formato_grabacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese formato de grabacion','required': 'required'}),
            'productor_emp_produc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese productor o empresa productora','required': 'required'}),
            'nom_director': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre del director','required': 'required'}),
            'sinopsis_corta': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Ingrese storyline / sinopsis corta', 'required': 'required'}),
            'locaciones_rodaje': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese locaciones de rodaje','required': 'required'}),
            'beneficiario_fdc': forms.RadioSelect(attrs={'class': 'form-check-input', 'id': 'id_beneficiario_fdc','required': 'required'}),
            'anio_fdc': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_anio_fdc'}),
            'certificacion_fdc': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_certificacion_fdc'}),
            'exhibicion_salas': forms.RadioSelect(attrs={'class': 'form-check-input', 'id': 'id_exhibicion_salas','required': 'required'}),
            'plataformas_exhibicion': forms.RadioSelect(attrs={'class': 'form-check-input', 'id': 'id_plataformas_exhibicion','required': 'required'}),
            'si_plataforma': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_si_plataforma'}),
            'resolucion_cpn': forms.NumberInput(attrs={'class': 'form-control','required': 'required'}),
            'fecha_resolucion_cpn': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','required': 'required'}),
            'certificacion_cpn': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_certificacion_cpn','required': 'required'}),
            'acta_clasificacion': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_acta_clasificacion'}),
            'tipo_persona':forms.RadioSelect(attrs={'class': 'form-check-input', 'id': 'id_tipo_persona'}),
            'autorizacion_uso': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_autorizacion_uso','required': 'required'}),
            'enlace_vimeo':forms.URLInput(attrs={'class': 'form-control','placeholder': 'Ingrese el enlace de Vimeo','required': 'required'}),
            'contrasena_vimeo': forms.PasswordInput(attrs={'class': 'form-control','id': 'id_contrasena_vimeo','placeholder': 'Ingrese la contraseña de Vimeo','required': 'required'}),
            'principales_festivales': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese los principales festivales','required': 'required'}),
            'nombre_productor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre productor','required': 'required'}),
            'celular_productor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese celular productor','required': 'required'}),
            'domicilio_productor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese domicilio productor','required': 'required'}),
            'correo_productor': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese correo productor','required': 'required'}),
            'postulado_antes': forms.RadioSelect(attrs={'class': 'form-check-input', 'id': 'id_postulado_antes'}),
            'certificacion_cumplimiento': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_certificacion_cumplimiento','required': 'required'}),
            'acepta_tyc':forms.RadioSelect(attrs={'class': 'form-check-input', 'id': 'id_acepta_tyc'}),
        }

    
        
class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = ["comentario", "recomendacion"]
        widgets = {
            "comentario": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Escribe tu evaluación aquí...",
                "rows": 4
            }),
            "recomendacion": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_comentario(self):
        comentario = self.cleaned_data.get("comentario")
        if comentario and len(comentario.strip()) < 50:
            raise forms.ValidationError("El comentario debe tener al menos 50 caracteres.")
        return comentario

class RegistroUsuarioForm(UserCreationForm):
    username = forms.CharField(
        label="NIT (Usuario)",
        max_length=11,
        min_length=8,
        help_text="Ingrese su NIT o cédula (8 a 11 dígitos numéricos).",
        widget=forms.TextInput(attrs={"placeholder": "Ej: 1031123075", "class": "form-control"})
    )
    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Ej: micorreo@dominio.com"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not re.match(r"^\d{8,11}$", username):
            raise forms.ValidationError("El NIT debe tener entre 8 y 11 dígitos numéricos.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo.")
        return email

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
