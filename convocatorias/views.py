from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Postulacion
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
