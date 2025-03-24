from django.urls import path
from .views import (
    postulacion_publica,
    postulacion_exitosa,
    verificar_postulacion,
    lista_postulaciones_admin,
    asignar_evaluadores,
    evaluar_postulacion,
    postulaciones_asignadas,
    revisar_evaluaciones,
    generar_acta,
    detalle_acta,
    lista_actas,
    agregar_postulacion_acta,
    quitar_postulacion_acta,
    detalle_postulacion
)

urlpatterns = [
    path('postulacion/', postulacion_publica, name='postulacion_publica'),
    path('postulacion-exitosa/', postulacion_exitosa, name='postulacion_exitosa'),
    path('verificar-postulacion/<int:postulacion_id>/', verificar_postulacion, name='verificar_postulacion'),  # 🔹 Nueva ruta
    path('lista-postulaciones/', lista_postulaciones_admin, name='lista_postulaciones_admin'),  # ✅ Nueva ruta
    path('asignar-evaluadores/<int:postulacion_id>/', asignar_evaluadores, name='asignar_evaluadores'),  # ✅ Nueva URL
    path('evaluar-postulacion/<int:postulacion_id>/', evaluar_postulacion, name='evaluar_postulacion'),
    path('postulaciones-asignadas/', postulaciones_asignadas, name='postulaciones_asignadas'),
    path('lista-postulaciones/', lista_postulaciones_admin, name='lista_postulaciones_admin'),
    path('revisar-evaluaciones/<int:postulacion_id>/', revisar_evaluaciones, name='revisar_evaluaciones'),
    path('generar-acta/', generar_acta, name='generar_acta'),
    path('detalle-acta/<int:acta_id>/', detalle_acta, name='detalle_acta'),
    path('actas/', lista_actas, name='lista_actas'),
    path('acta/<int:acta_id>/agregar/<int:postulacion_id>/', agregar_postulacion_acta, name='agregar_postulacion_acta'),
    path('acta/<int:acta_id>/quitar/<int:postulacion_id>/', quitar_postulacion_acta, name='quitar_postulacion_acta'),
    path('detalle-postulacion/<int:postulacion_id>/', detalle_postulacion, name='detalle_postulacion'),
]
