from django import forms
from .models import Postulacion

class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ['correo','titulo', 'anio_produccion','duracion','formato_grabacion','productor_emp_produc',
                  'nom_director','sinopsis_corta','locaciones_rodaje','beneficiario_fdc', 'anio_fdc',
                  'certificacion_fdc','exhibicion_salas','plataformas_exhibicion', 'si_plataforma','resolucion_cpn',
                  'fecha_resolucion_cpn','certificacion_cpn', 'acta_clasificacion','tipo_persona','autorizacion_uso',
                  'enlace_vimeo','contrasena_vimeo','principales_festivales','nombre_productor','celular_productor',
                  'domicilio_productor','correo_productor','postulado_antes','certificacion_cumplimiento','acepta_tyc',
                 ]  # Excluir 'usuario' y 'estado'

        widgets = {
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el correo','required': 'required'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_titulo','placeholder': 'Ingrese el titulo','required': 'required'}),
            'anio_produccion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese año de produccion','required': 'required'}),
            'duracion': forms.TimeInput(attrs={'class': 'form-control', 'id': 'id_duracion','placeholder': 'Ingrese la doracion del corto HH:MM','required': 'required'}, format='%H:%M'),
            'formato_grabacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese formato de grabacion','required': 'required'}),
            'productor_emp_produc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese productor o empresa productora','required': 'required'}),
            'nom_director': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre del director','required': 'required'}),
            'sinopsis_corta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese storyline / sinopsis corta','required': 'required'}),
            'locaciones_rodaje': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese locaciones de rodaje','required': 'required'}),
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
            'autorizacion_uso': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_autorizacion_uso'}),
            'enlace_vimeo':forms.URLInput(attrs={'class': 'form-control','placeholder': 'Ingrese el enlace de Vimeo'}),
            'contrasena_vimeo': forms.PasswordInput(attrs={'class': 'form-control','id': 'id_contrasena_vimeo','placeholder': 'Ingrese la contraseña de Vimeo'}),
            'principales_festivales': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese los principales festivales'}),
            'nombre_productor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre productor'}),
            'celular_productor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese celular productor'}),
            'domicilio_productor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese domicilio productor'}),
            'correo_productor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese correo productor'}),
            'postulado_antes': forms.RadioSelect(attrs={'class': 'form-check-input', 'id': 'id_postulado_antes'}),
            'certificacion_cumplimiento': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_certificacion_cumplimiento'}),
            'acepta_tyc':forms.RadioSelect(attrs={'class': 'form-check-input', 'id': 'id_acepta_tyc'}),
        }
