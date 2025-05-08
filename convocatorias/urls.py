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
    detalle_postulacion,
    actualizar_recomendacion,
    recordar_evaluacion,
    solicitar_cambio_comentario,
    generar_pdfs_acta,
    actas_pendientes_evaluador,
    actualizar_estado_acta,
    aprobar_acta_evaluador,
    firmar_acta,
    banco_cortos_publico,
    banco_cortos_embed,
    servir_archivo_media,
    ver_archivos,
    login_programacion_web,
    LoginProgramacionView,
    registro_usuario,
)

from django.contrib.auth import views as auth_views  # 📌 Para recuperación de contraseña

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
    path('actualizar-recomendacion/', actualizar_recomendacion, name='actualizar_recomendacion'),
    path("recordar-evaluacion/", recordar_evaluacion, name="recordar_evaluacion"),
    path("solicitar-cambio-comentario/", solicitar_cambio_comentario, name="solicitar_cambio_comentario"),
    path('generar-pdfs-acta/<int:acta_id>/', generar_pdfs_acta, name='generar_pdfs_acta'),
    path('actas-pendientes/', actas_pendientes_evaluador, name='actas_pendientes_evaluador'),
    path('acta/<int:acta_id>/actualizar-estado/', actualizar_estado_acta, name='actualizar_estado_acta'),
    path('actas/aprobar/<int:acta_id>/', aprobar_acta_evaluador, name='aprobar_acta_evaluador'),
    path('actas/<int:acta_id>/firmar/', firmar_acta, name='firmar_acta'),
    path('banco-cortos/', banco_cortos_publico, name='banco_cortos'),
    path('banco-cortos/embed/', banco_cortos_embed, name='banco_cortos_embed'),
    path('descargar/<path:ruta_archivo>/', servir_archivo_media, name='descargar_archivo'),
    path('admin/ver-archivos/', ver_archivos, name='ver_archivos'),

     # 🧩 Login API y web
    path('api/login-programacion/', LoginProgramacionView.as_view(), name='login_programacion_api'),
    path('login-programacion-web/', login_programacion_web, name='login_programacion_web'),

    # 🧩 Recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="programaciones/password_reset_form.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="programaciones/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="programaciones/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="programaciones/password_reset_complete.html"), name='password_reset_complete'),
    path('registro/', registro_usuario, name='registro_usuario'),
]
