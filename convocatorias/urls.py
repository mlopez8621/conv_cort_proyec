from django.urls import path
from .views import postulacion_publica,postulacion_exitosa

urlpatterns = [
    path('postulacion/', postulacion_publica, name='postulacion_publica'),
    path('postulacion-exitosa/', postulacion_exitosa, name='postulacion_exitosa'),
]
