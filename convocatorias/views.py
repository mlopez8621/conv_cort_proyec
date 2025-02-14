from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Postulacion, Evaluador
from .forms import PostulacionForm

def postulacion_publica(request):
    if request.method == 'POST':
        form = PostulacionForm(request.POST, request.FILES)
        if form.is_valid():
            postulacion = form.save(commit=False)
            
            # Asignar el usuario "postulante" a la postulación
            postulacion.usuario = User.objects.get(username='postulante')
            
            postulacion.save()
            return redirect('postulacion_exitosa')  # Redirige tras éxito
    else:
        form = PostulacionForm()
    
    return render(request, 'convocatorias/postulacion_publica.html', {'form': form})

def postulacion_exitosa(request):
    return render(request, 'convocatorias/postulacion_exitosa.html')

# ✅ Función para restringir acceso solo a administradores
def es_admin(user):
    return user.is_staff  # Solo los admins pueden verificar postulaciones

@login_required
@user_passes_test(es_admin)
def verificar_postulacion(request, postulacion_id):
    """
    Vista que permite a los administradores revisar una postulación y aprobarla o rechazarla.
    """
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)

    if request.method == "POST":
        comentario_admin = request.POST.get("comentario_admin", "")

        if "aprobar" in request.POST:
            postulacion.estado = "evaluacion"
            postulacion.revisado_por_admin = True
            postulacion.save()

            # Enviar correo de aprobación al productor
            send_mail(
                subject="Postulación Aprobada",
                message=f"Su postulación '{postulacion.titulo}' ha sido aprobada y enviada a evaluación.\n\nComentario del administrador: {comentario_admin}",
                from_email="automatizacionprocesos@proimagenescolombia.com",
                recipient_list=[postulacion.correo_productor],
            )

            return redirect('asignar_evaluadores', postulacion_id=postulacion.id)  # Redirige a la vista de asignación

        elif "rechazar" in request.POST:
            postulacion.estado = "rechazado"
            postulacion.revisado_por_admin = True
            postulacion.comentario_admin = comentario_admin
            postulacion.save()

            # Enviar correo de rechazo
            send_mail(
                subject="Postulación Aprobada",
                message=f"Su postulación '{postulacion.titulo}' ha sido aprobada.",
                from_email="automatizacionprocesos@proimagenescolombia.com",
                recipient_list=[postulacion.correo_productor],
            )

            return redirect('lista_postulaciones_admin')  # Redirige a la lista de postulaciones

    return render(request, 'convocatorias/verificar_postulacion.html', {'postulacion': postulacion})

@login_required
@user_passes_test(es_admin)
def lista_postulaciones_admin(request):
    """
    Vista que muestra todas las postulaciones para los administradores.
    """
    postulaciones = Postulacion.objects.all()
    return render(request, 'convocatorias/lista_postulaciones_admin.html', {'postulaciones': postulaciones})

def asignar_evaluadores(request, postulacion_id):
    """
    Vista que permite asignar evaluadores a una postulación.
    """
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)

    if request.method == "POST":
        evaluadores_ids = request.POST.getlist('evaluadores')  # Lista de evaluadores seleccionados
        for evaluador_id in evaluadores_ids:
            evaluador = Evaluador.objects.get(id=evaluador_id)
            postulacion.evaluadores.add(evaluador)

        return redirect('verificar_postulacion', postulacion_id=postulacion.id)

    evaluadores = Evaluador.objects.all()
    return render(request, 'convocatorias/asignar_evaluadores.html', {'postulacion': postulacion, 'evaluadores': evaluadores})
