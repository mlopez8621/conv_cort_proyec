from django.urls import path
from .views import (
    postulacion_publica,
    postulacion_exitosa,
    verificar_postulacion,
    lista_postulaciones_admin,
    asignar_evaluadores,
    evaluar_postulacion,
    postulaciones_asignadas
)    

urlpatterns = [
    path('postulacion/', postulacion_publica, name='postulacion_publica'),
    path('postulacion-exitosa/', postulacion_exitosa, name='postulacion_exitosa'),
    path('verificar-postulacion/<int:postulacion_id>/', verificar_postulacion, name='verificar_postulacion'),  # 🔹 Nueva ruta
    path('lista-postulaciones/', lista_postulaciones_admin, name='lista_postulaciones_admin'),  # ✅ Nueva ruta
    path('asignar-evaluadores/<int:postulacion_id>/', asignar_evaluadores, name='asignar_evaluadores'),  # ✅ Nueva URL
    path('evaluar-postulacion/<int:postulacion_id>/', evaluar_postulacion, name='evaluar_postulacion'),
    path('postulaciones-asignadas/', postulaciones_asignadas, name='postulaciones_asignadas'),
]
