from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Postulacion, Evaluador, Evaluacion, PostulacionEvaluadores
from .forms import PostulacionForm
from .forms import EvaluacionForm
from django.http import HttpResponseRedirect

def postulacion_publica(request):
    print("🔹 Entrando a postulacion_publica")  # 🔥 Debug

    if request.method == 'POST':
        print("🔹 Se recibió un POST request")  # 🔥 Debug
        print(f"🔹 Datos recibidos: {request.POST}")  # 🔥 Debug

        form = PostulacionForm(request.POST, request.FILES)
        if form.is_valid():
            print("✅ El formulario es válido")  # 🔥 Debug

            postulacion = form.save(commit=False)

            try:
                postulacion.usuario = User.objects.get(username='postulante')
                print(f"✅ Usuario encontrado: {postulacion.usuario}")  # 🔥 Debug
                
                postulacion.save()
                print("✅ Postulación guardada correctamente")  # 🔥 Debug

                return redirect('postulacion_exitosa')
            except User.DoesNotExist:
                print("❌ ERROR: Usuario 'postulante' no encontrado")  # 🔥 Debug
                messages.error(request, "Error: No se encontró el usuario 'postulante'. Contacte con el administrador.")
        else:
            print("❌ ERROR: Formulario no válido")  # 🔥 Debug
            print(form.errors.as_json())  # 🔥 Debug para ver los errores

    else:
        print("🔹 Se recibió un GET request")  # 🔥 Debug
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
        comentario_admin = request.POST.get("comentario_admin", "").strip()

        # Guarda siempre el comentario antes de cualquier cambio de estado
        postulacion.comentario_admin = comentario_admin
        postulacion.revisado_por_admin = True

        if "aprobar" in request.POST:
            postulacion.estado = "evaluacion"
            postulacion.revisado_por_admin = True
            postulacion.save()

            # Enviar correo de aprobación al productor
            #send_mail(
            #    subject="Postulación Aprobada",
            #    message=f"Su postulación '{postulacion.titulo}' ha sido aprobada y enviada a evaluación.\n\nComentario del administrador: {comentario_admin}",
            #    from_email="automatizacionprocesos@proimagenescolombia.com",
            #    recipient_list=[postulacion.correo_productor],
            #)

            return redirect('asignar_evaluadores', postulacion_id=postulacion.id)  # Redirige a la vista de asignación

        elif "rechazar" in request.POST:
            postulacion.estado = "rechazado"
            postulacion.save()

            # Enviar correo de rechazo
            #send_mail(
            #    subject="Postulación Aprobada",
            #    message=f"Su postulación '{postulacion.titulo}' ha sido aprobada.",
            #    from_email="automatizacionprocesos@proimagenescolombia.com",
            #    recipient_list=[postulacion.correo_productor],
            #)

            return render(request, 'convocatorias/rechazo_exitoso.html', {'postulacion': postulacion})  

    return render(request, 'convocatorias/verificar_postulacion.html', {'postulacion': postulacion})

@login_required
@user_passes_test(es_admin)
def asignar_evaluadores(request, postulacion_id):
    """
    Vista que permite asignar evaluadores a una postulación.
    """
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)
    print(f"🔹 Postulación encontrada: {postulacion} (ID: {postulacion.id})")  # 🔍 Debug

    if request.method == "POST":
        evaluadores_ids = request.POST.getlist('evaluadores')  # Lista de evaluadores seleccionados
        print(f"🔹 Evaluadores seleccionados: {evaluadores_ids}")  # 🔍 Debug

        if not evaluadores_ids:
            messages.error(request, "❌ No seleccionaste ningún evaluador.")
            return redirect('verificar_postulacion', postulacion_id=postulacion.id)

        asignados = 0  # Contador de asignaciones exitosas
        ya_asignados = 0  # Contador de evaluadores ya asignados

        for evaluador_id in evaluadores_ids:
            try:
                evaluador = Evaluador.objects.get(id=evaluador_id)
                print(f"✅ Evaluador encontrado: {evaluador.nombre} (ID: {evaluador.id})")  # 🔍 Debug

                # Verificar si la asignación ya existe
                if PostulacionEvaluadores.objects.filter(postulacion=postulacion, evaluador=evaluador).exists():
                    print(f"⚠️ Asignación ya existe para {evaluador.nombre}")
                    ya_asignados += 1
                else:
                    PostulacionEvaluadores.objects.create(postulacion=postulacion, evaluador=evaluador)
                    print(f"✅ Asignación creada: {evaluador.nombre} → {postulacion.titulo}")  # 🔍 Debug
                    asignados += 1

            except Evaluador.DoesNotExist:
                print(f"❌ ERROR: Evaluador con ID {evaluador_id} no existe.")  # 🔍 Debug

        print(f"🔹 Total Asignados: {asignados}, Ya Asignados: {ya_asignados}")  # 🔍 Debug

        # Enviar los datos a la plantilla correctamente
        return render(request, 'convocatorias/asignacion_exitosa.html', {
            'postulacion': postulacion,
            'asignados': asignados,
            'ya_asignados': ya_asignados
        })

    evaluadores = Evaluador.objects.all()
    return render(request, 'convocatorias/asignar_evaluadores.html', {'postulacion': postulacion, 'evaluadores': evaluadores})


@login_required
def evaluar_postulacion(request, postulacion_id):
    """
    Vista para evaluar una postulación, pero restringida a las que el evaluador tiene asignadas.
    """
    usuario = request.user
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)

    # 🔹 Obtener el evaluador relacionado con este usuario
    try:
        evaluador = Evaluador.objects.get(usuario=usuario)
    except Evaluador.DoesNotExist:
        messages.error(request, "No tienes permiso para evaluar esta postulación.")
        return redirect('postulaciones_asignadas')

    # 🔹 Verificar si el evaluador tiene asignada esta postulación
    asignacion_existe = PostulacionEvaluadores.objects.filter(postulacion=postulacion, evaluador=evaluador).exists()
    
    if not asignacion_existe:
        messages.error(request, "No tienes permiso para evaluar esta postulación.")
        return redirect('postulaciones_asignadas')

    # 🔹 Obtener la evaluación existente o crear una nueva
    evaluacion, created = Evaluacion.objects.get_or_create(postulacion=postulacion, evaluador=evaluador)

    if request.method == "POST":
        form = EvaluacionForm(request.POST, instance=evaluacion)
        if form.is_valid():
            form.save()
            return render(request, "convocatorias/evaluacion_exitosa.html", {
                "postulacion": postulacion
            })  # ✅ Muestra la página de confirmación antes de redirigir
    else:
        form = EvaluacionForm(instance=evaluacion)

    return render(request, "convocatorias/evaluar_postulacion.html", {
        "postulacion": postulacion,
        "form": form  # ✅ Se pasa el formulario a la plantilla
    })


@login_required
def postulaciones_asignadas(request):
    usuario = request.user
    print(f"🔹 Usuario autenticado: {usuario.username} (ID: {usuario.id})")  # 🔹 Debug

    # Buscar el evaluador correspondiente al usuario autenticado
    try:
        evaluador = Evaluador.objects.get(usuario=usuario)
        print(f"✅ Evaluador encontrado: {evaluador} (ID: {evaluador.id})")  # 🔹 Debug
    except Evaluador.DoesNotExist:
        print("❌ Evaluador no encontrado para este usuario.")  # 🔹 Debug
        return render(request, 'convocatorias/postulaciones_asignadas.html', {'postulaciones': []})

    # Obtener las postulaciones asignadas al evaluador
    postulaciones = Postulacion.objects.filter(
        id__in=PostulacionEvaluadores.objects.filter(evaluador=evaluador).values_list("postulacion_id", flat=True)
    )

    print(f"✅ Postulaciones encontradas para el evaluador {evaluador.nombre}: {postulaciones}")

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

@login_required
@user_passes_test(es_admin)
def lista_postulaciones_admin(request):
    """
    Vista que muestra todas las postulaciones para los administradores con paginación.
    """
    postulaciones_list = Postulacion.objects.all().order_by('-id')  # Ordena por ID descendente
    paginator = Paginator(postulaciones_list, 5)  # 5 postulaciones por página

    page_number = request.GET.get('page')
    postulaciones = paginator.get_page(page_number)

    return render(request, 'convocatorias/lista_postulaciones_admin.html', {'postulaciones': postulaciones})


@login_required
def postulaciones_asignadas(request):
    usuario = request.user
    print(f"🔹 Usuario autenticado: {usuario.username} (ID: {usuario.id})")  # 🔹 Debug

    # Intentar obtener el evaluador correspondiente al usuario autenticado
    try:
        evaluador = Evaluador.objects.get(usuario=usuario)
        print(f"✅ Evaluador encontrado: {evaluador} (ID: {evaluador.id})")  # 🔹 Debug
    except Evaluador.DoesNotExist:
        print("❌ Evaluador no encontrado para este usuario.")  # 🔹 Debug
        return render(request, 'convocatorias/postulaciones_asignadas.html', {'postulaciones': [], 'mensaje': "No tienes asignaciones de evaluación."})

    # Obtener postulaciones asignadas al evaluador usando la tabla intermedia
    postulaciones_list = Postulacion.objects.filter(
        id__in=PostulacionEvaluadores.objects.filter(evaluador=evaluador).values_list("postulacion_id", flat=True)
    )

    print(f"✅ Postulaciones encontradas para el evaluador {evaluador.nombre}: {postulaciones_list}")  # 🔹 Debug

    # Paginar resultados (5 postulaciones por página)
    paginator = Paginator(postulaciones_list, 5)
    page_number = request.GET.get("page")
    postulaciones = paginator.get_page(page_number)

    return render(
        request,
        "convocatorias/postulaciones_asignadas.html",
        {"postulaciones": postulaciones}
    )




