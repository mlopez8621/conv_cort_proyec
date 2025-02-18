from django.contrib import admin
from .models import Postulacion, Evaluacion, Veredicto, Evaluador, PostulacionEvaluadores

class EvaluadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'get_username')

    def get_username(self, obj):
        return obj.usuario.username  # Accede correctamente a `username` del usuario relacionado
    get_username.admin_order_field = 'usuario__username'  # Para permitir ordenamiento
    get_username.short_description = 'Username'  # Nombre visible en la tabla

class PostulacionEvaluadoresAdmin(admin.ModelAdmin):
    list_display = ('evaluador', 'postulacion')  # Campos visibles en la tabla del admin
    search_fields = ('evaluador__nombre', 'postulacion__titulo')  # Permite buscar por nombre y título
    list_filter = ('evaluador', 'postulacion')  # Agrega filtros en la barra lateral    

admin.site.register(Evaluador, EvaluadorAdmin)
admin.site.register(PostulacionEvaluadores, PostulacionEvaluadoresAdmin)
admin.site.register(Postulacion)
admin.site.register(Evaluacion)
admin.site.register(Veredicto)
