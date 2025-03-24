from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Postulacion, Evaluador, Evaluacion, PostulacionEvaluadores, ActaEvaluacion
from .forms import PostulacionForm
from .forms import EvaluacionForm
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import calendar
from datetime import datetime
import locale

# Establecer el locale para obtener nombres de meses en español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Linux/Mac
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Windows
    except locale.Error:
        pass  # En caso de que no funcione, puedes manejarlo o mostrar meses manualmente

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
                print(f"✅ Evaluador encontrado: {evaluador.usuario.first_name} {evaluador.usuario.last_name} (ID: {evaluador.id})")  # 🔍 Debug

                # Verificar si la asignación ya existe
                if PostulacionEvaluadores.objects.filter(postulacion=postulacion, evaluador=evaluador).exists():
                    print(f"⚠️ Asignación ya existe para {evaluador.usuario.first_name} {evaluador.usuario.last_name}")
                    ya_asignados += 1
                else:
                    PostulacionEvaluadores.objects.create(postulacion=postulacion, evaluador=evaluador)
                    print(f"✅ Asignación creada: {evaluador.usuario.first_name} {evaluador.usuario.last_name} → {postulacion.titulo}")  # 🔍 Debug
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
            messages.error(request, "El comentario debe tener al menos 50 caracteres.")  # 🔹 Mensaje de error
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
            return render(request, "convocatorias/login.html")  # Redirigir al login si falla
        
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

    # Generar nombres de meses en español (ej: [(1, "Enero"), (2, "Febrero"), ...])
    nombres_meses = [(i, datetime(1900, i, 1).strftime('%B').capitalize()) for i in range(1, 13)]

    context = {
        'postulaciones': postulaciones,
        'meses': nombres_meses,
        'now': datetime.now(),
    }

    return render(request, 'convocatorias/lista_postulaciones_admin.html', context)


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

    print(f"✅ Postulaciones encontradas para el evaluador {evaluador.usuario.first_name}: {postulaciones_list}")  # 🔹 Debug

    # Paginar resultados (5 postulaciones por página)
    paginator = Paginator(postulaciones_list, 5)
    page_number = request.GET.get("page")
    postulaciones = paginator.get_page(page_number)

    return render(
        request,
        "convocatorias/postulaciones_asignadas.html",
        {"postulaciones": postulaciones}
    )

@login_required
@csrf_exempt
def revisar_evaluaciones(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)
    evaluaciones = Evaluacion.objects.filter(postulacion=postulacion)
    asignaciones = PostulacionEvaluadores.objects.filter(postulacion=postulacion)

    evaluaciones_dict = {
        evaluacion.evaluador.id: evaluacion
        for evaluacion in evaluaciones
    }

    acta = postulacion.acta  # Asegúrate de que exista esta relación

    if request.method == "POST":
        comentario_final = request.POST.get("comentario_final")

        recomendaciones_si = evaluaciones.filter(recomendacion="si").count()
        recomendaciones_no = evaluaciones.filter(recomendacion="no").count()

        if recomendaciones_si > recomendaciones_no:
            postulacion.estado = "aprobado"
        else:
            postulacion.estado = "rechazado"

        postulacion.comentario_final = comentario_final
        postulacion.save()

        return redirect("detalle_acta", acta_id=acta.id)

    return render(request, "convocatorias/revisar_evaluaciones.html", {
        "postulacion": postulacion,
        "evaluaciones_dict": evaluaciones_dict,
        "asignaciones": asignaciones,
        "acta": acta,  # 👈 Esto es lo que faltaba
    })

@login_required
@csrf_exempt
def actualizar_recomendacion(request, evaluacion_id):
    if not request.user.is_staff:
        return JsonResponse({"success": False, "error": "Acceso denegado."}, status=403)

    if request.method == "POST":
        data = json.loads(request.body)
        nueva_recomendacion = data.get("recomendacion")

        try:
            evaluacion = Evaluacion.objects.get(id=evaluacion_id)
            evaluacion.recomendacion = nueva_recomendacion
            evaluacion.save()
            return JsonResponse({"success": True})
        except Evaluacion.DoesNotExist:
            return JsonResponse({"success": False, "error": "Evaluación no encontrada."}, status=404)

    return JsonResponse({"success": False, "error": "Método no permitido."}, status=405)

@login_required
@csrf_exempt
def notificar_evaluador(request, evaluacion_id):
    if not request.user.is_staff:
        return JsonResponse({"success": False, "error": "Acceso denegado."}, status=403)

    if request.method == "POST":
        try:
            evaluacion = Evaluacion.objects.get(id=evaluacion_id)
            evaluador = evaluacion.evaluador
            email = evaluador.usuario.email  # Tomar el email desde la tabla User

            send_mail(
                subject="🔔 Ajuste requerido en tu evaluación",
                message=f"Hola {evaluador.usuario.first_name},\n\n"
                        f"Se ha cambiado la recomendación de tu evaluación. "
                        f"Por favor revisa y ajusta tu comentario si es necesario.\n\n"
                        f"Ingresar aquí: http://localhost:8000",
                from_email="automatizacionprocesos@proimagenescolombia.com",
                recipient_list=[email],
                fail_silently=False,
            )

            return JsonResponse({"success": True})
        except Evaluacion.DoesNotExist:
            return JsonResponse({"success": False, "error": "Evaluación no encontrada."}, status=404)

    return JsonResponse({"success": False, "error": "Método no permitido."}, status=405)

def generar_acta(request):
    if request.method == "POST":
        mes = int(request.POST['mes'])
        anio = int(request.POST['anio'])

        # Verificar si ya existe un acta para ese mes y año
        if ActaEvaluacion.objects.filter(mes=mes, anio=anio).exists():
            messages.error(request, "⚠️ Ya existe un acta para ese periodo. No puedes crear una duplicada.")
            return redirect('lista_postulaciones_admin')  # O la vista donde esté el modal

        # Obtener postulaciones del periodo
        postulaciones = Postulacion.objects.filter(
            fecha_postulacion__month=mes,
            fecha_postulacion__year=anio,
            estado='evaluacion'
        )

        acta = ActaEvaluacion.objects.create(mes=mes, anio=anio, creada_por=request.user)
        postulaciones.update(acta=acta)

        messages.success(request, "✅ Acta creada exitosamente con postulaciones del periodo seleccionado.")
        return redirect('detalle_acta', acta.id)

    return redirect('lista_postulaciones_admin')

from django.shortcuts import render, get_object_or_404
from .models import ActaEvaluacion

@login_required
@user_passes_test(es_admin)
def detalle_acta(request, acta_id):
    acta = get_object_or_404(ActaEvaluacion, pk=acta_id)

    postulaciones_asociadas = Postulacion.objects.filter(acta=acta)
    postulaciones_disponibles = Postulacion.objects.filter(
        acta__isnull=True,
        fecha_postulacion__month=acta.mes,
        fecha_postulacion__year=acta.anio,
        estado='evaluacion'
    )
    resumen_postulaciones = []
    for postulacion in postulaciones_asociadas:
        evaluadores_asignados = postulacion.evaluadores.count()
        evaluaciones = postulacion.evaluaciones.all()
        total = evaluaciones.count()
        faltan = evaluadores_asignados - total

        si = evaluaciones.filter(recomendacion='si').count()
        no = evaluaciones.filter(recomendacion='no').count()
        discusion = evaluaciones.filter(recomendacion='discusion').count()

        if evaluadores_asignados == 0:
            estado = 'sin_evaluadores'
        elif faltan > 0:
            estado = 'faltan'
        else:
            estado = 'aprobada' if si >= ((total // 2) + 1) else 'no_aprobada'

        resumen_postulaciones.append({
            'postulacion': postulacion,
            'evaluaciones': evaluaciones,
            'conteo': {
                'si': si,
                'no': no,
                'discusion': discusion,
                'faltan': faltan  # 👈 lo enviamos al template
            },
            'estado_aprobacion': estado
        })
    
    context = {
        'acta': acta,
        'resumen_postulaciones': resumen_postulaciones,
        'postulaciones_disponibles': postulaciones_disponibles,

    }   
    return render(request, 'convocatorias/detalle_acta.html', context)

@login_required
@user_passes_test(es_admin)
def lista_actas(request):
    actas = ActaEvaluacion.objects.all().order_by('-anio', '-mes')
    return render(request, 'convocatorias/lista_actas.html', {'actas': actas})

@login_required
@user_passes_test(es_admin)
def agregar_postulacion_acta(request, acta_id, postulacion_id):
    acta = get_object_or_404(ActaEvaluacion, pk=acta_id)
    postulacion = get_object_or_404(Postulacion, pk=postulacion_id)
    postulacion.acta = acta
    postulacion.save()
    messages.success(request, "✅ Postulación agregada al acta.")
    return redirect('detalle_acta', acta_id=acta_id)

@login_required
@user_passes_test(es_admin)
def quitar_postulacion_acta(request, acta_id, postulacion_id):
    postulacion = get_object_or_404(Postulacion, pk=postulacion_id, acta_id=acta_id)
    postulacion.acta = None
    postulacion.save()
    messages.success(request, "❌ Postulación removida del acta.")
    return redirect('detalle_acta', acta_id=acta_id)

@login_required
@user_passes_test(es_admin)
def detalle_postulacion(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)
    asignaciones = postulacion.evaluadores.all()
    evaluaciones = postulacion.evaluaciones.all()

    evaluadores_estado = []
    for asignado in asignaciones:
        evaluacion = evaluaciones.filter(evaluador=asignado).first()
        evaluadores_estado.append({
            'evaluador': asignado,
            'evaluacion': evaluacion
        })

    context = {
        'postulacion': postulacion,
        'evaluadores_estado': evaluadores_estado,
    }
    return render(request, 'convocatorias/detalle_postulacion.html', context)








