from django.http import HttpResponse
from django.shortcuts import render
from .models import Solicitud
from django.contrib.auth.decorators import login_required

@login_required
def solicitudes(request):
    database = Solicitud.objects.all().order_by('-fecha_solicitud')
    
    return render(
        request, 'index.html', context={'pedidos': database}
    )
    


# crear 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Solicitud
from .forms import SolicitudForm

def pedido_crear(request):
    form = SolicitudForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('solicitudes')   #  CAMBIO
    return render(request, 'form.html', {'form': form})

def pedido_editar(request, id):
    pedido = get_object_or_404(Solicitud, id=id)
    form = SolicitudForm(request.POST or None, instance=pedido)
    if form.is_valid():
        form.save()
        return redirect('solicitudes')   #  CAMBIO
    return render(request, 'form.html', {'form': form})

def pedido_eliminar(request, id):
    pedido = get_object_or_404(Solicitud, id=id)
    pedido.delete()
    return redirect('solicitudes')       #  CAMBIO


# autocompleatdo 

from django.http import JsonResponse
from .models import Solicitud

def buscar_por_dun(request):
    cod_dun = request.GET.get("cod_dun")

    if not cod_dun:
        return JsonResponse({}, status=400)

    # Tomamos la PRIMERA coincidencia
    producto = Solicitud.objects.filter(cod_dun=cod_dun).first()

    if producto:
        return JsonResponse({
            "cod_ean": producto.cod_ean,
            "cod_sistema": producto.cod_sistema,
            "descripcion": producto.descripcion,
        })

    return JsonResponse({}, status=404)



# admin 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def crear_superusuario(request):
    if request.method == 'POST':
        User.objects.create_superuser(
            username=request.POST['username'],
            password=request.POST['password'],
            email=request.POST.get('email')
        )
        return redirect('login')

    return render(request, 'crear_superusuario.html')


# resumen dedicado a mi mama 
from django.db.models import Sum
from .models import Solicitud

def resumen_bsf(request):
    resumen = (
        Solicitud.objects
        .values(
            'cod_dun',
            'cod_ean',
            'cod_sistema',
            'descripcion'
        )
        .annotate(
            total_bsf=Sum('cant_enviada_bsf')
        )
        .order_by('cod_dun')
    )

    return render(request, 'resumen_bsf.html', {
        'resumen': resumen
    })
