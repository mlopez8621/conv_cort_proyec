from django.contrib import admin
from .models import Postulacion, Evaluacion, Veredicto, Evaluador, PostulacionEvaluadores

class EvaluadorAdmin(admin.ModelAdmin):
    list_display = ('get_nombre', 'get_correo', 'get_username')  # ✅ Métodos correctos

    def get_nombre(self, obj):
        return f"{obj.usuario.first_name} {obj.usuario.last_name}"  # ✅ Obtener nombre del usuario relacionado
    get_nombre.admin_order_field = 'usuario__first_name'  # Habilita ordenamiento
    get_nombre.short_description = 'Nombre'

    def get_correo(self, obj):
        return obj.usuario.email  # ✅ Obtener correo del usuario relacionado
    get_correo.admin_order_field = 'usuario__email'
    get_correo.short_description = 'Correo Electrónico'

    def get_username(self, obj):
        return obj.usuario.username  # ✅ Obtener username
    get_username.admin_order_field = 'usuario__username'
    get_username.short_description = 'Username'

class PostulacionEvaluadoresAdmin(admin.ModelAdmin):
    list_display = ('evaluador', 'postulacion')  # Campos visibles en la tabla del admin
    search_fields = ('evaluador__nombre', 'postulacion__titulo')  # Permite buscar por nombre y título
    list_filter = ('evaluador', 'postulacion')  # Agrega filtros en la barra lateral    

admin.site.register(Evaluador, EvaluadorAdmin)
admin.site.register(PostulacionEvaluadores, PostulacionEvaluadoresAdmin)
admin.site.register(Postulacion)
admin.site.register(Evaluacion)
admin.site.register(Veredicto)
