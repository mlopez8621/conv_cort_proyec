from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Postulacion, Evaluador, Evaluacion
from .forms import PostulacionForm
from .forms import EvaluacionForm
from django.http import HttpResponseRedirect

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

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Postulacion, Evaluacion
from .forms import EvaluacionForm  # Importa el formulario

@login_required
def evaluar_postulacion(request, postulacion_id):
    """
    Vista para evaluar una postulación, pero restringida a las que el evaluador tiene asignadas.
    """
    usuario = request.user
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)

    # Verificar si el usuario tiene permiso para evaluar esta postulación
    evaluacion_asignada = Evaluacion.objects.filter(postulacion=postulacion, evaluador=usuario).exists()
    
    if not evaluacion_asignada:
        messages.error(request, "No tienes permiso para evaluar esta postulación.")
        return redirect('postulaciones_asignadas')

    # Verifica si ya existe una evaluación o crea una nueva
    evaluacion, created = Evaluacion.objects.get_or_create(postulacion=postulacion, evaluador=usuario)

    if request.method == "POST":
        form = EvaluacionForm(request.POST, instance=evaluacion)
        if form.is_valid():
            form.save()
            messages.success(request, "Evaluación guardada correctamente.")
            return redirect("postulaciones_asignadas")
    else:
        form = EvaluacionForm(instance=evaluacion)

    return render(request, "convocatorias/evaluar_postulacion.html", {
        "postulacion": postulacion,
        "form": form  # ✅ Agrega el formulario aquí
    })


@login_required
def postulaciones_asignadas(request):
    """
    Vista que muestra al evaluador solo las postulaciones que tiene asignadas.
    """
    usuario = request.user  # Obtener el usuario autenticado
    evaluaciones = Evaluacion.objects.filter(evaluador=usuario)  # Filtrar solo sus asignaciones
    postulaciones = [eva.postulacion for eva in evaluaciones]  # Obtener las postulaciones evaluadas

    return render(request, 'convocatorias/postulaciones_asignadas.html', {'postulaciones': postulaciones})

def custom_login(request):
    print("🔹 Entrando a custom_login")  # 🔥 Debug
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(f"Usuario autenticado: {user.username} (is_staff={user.is_staff})")
            
            # ✅ Si es administrador, redirigir a la lista de postulaciones
            if user.is_staff:
                print("Redirigiendo a lista_postulaciones_admin")  # 🔹 Debug
                return redirect("lista_postulaciones_admin")
            
            # ✅ Si es evaluador, redirigir a las postulaciones asignadas
            else:
                print("Redirigiendo a postulaciones_asignadas")  # 🔹 Debug
                return redirect("postulaciones_asignadas")
        
        else:
            print("❌ Error: Usuario o contraseña incorrectos")  # 🔹 Debug
            messages.error(request, "Usuario o contraseña incorrectos.")
            render(request, "convocatorias/login.html")  # Redirigir al login si falla
        
    print("❌ Redirigiendo a login (Acceso por GET)")  # 🔹 Debug
    return render(request, "convocatorias/login.html")
