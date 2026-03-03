# from pyexpat.errors import messages
from django.contrib import messages

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import Form_producto
from .models import Producto
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db import transaction

from django.utils import timezone
from datetime import timedelta


# Create your views here.

#el usuario debe estar autenticado para crear el producto
@login_required
# Vista para crear el producto
def crear_producto(request):

    # Eliminar borradores viejos del usuario
    tiempo_limite = timezone.now() - timedelta(minutes=15)

    Producto.objects.filter(
        user=request.user,
        estado_producto='borrador',
        fecha_creacion__lt=tiempo_limite
    ).delete()


    #procesar el formulario (Si se envía)
    if request.method == 'POST':
        #Se capturan los datos del producto y la imagen
        form = Form_producto(request.POST, request.FILES)

        #se valida si el formulario es valido
        if form.is_valid():
            accion = request.POST.get('accion')
            producto = form.save(commit=False)
            producto.user = request.user
            
            # Si quiere vista previa
            if accion == 'vista_previa':
                
                producto.estado_producto = 'borrador'
                producto.save()
                
                print(producto.imagen_producto)
                
                return redirect('vista_previa', producto.id)
            
            elif accion == 'cancelar':
                return redirect('tienda_usuario')

            # Si quiere guardar directo
            elif accion == 'guardar':
                producto.estado_producto = 'publicado'
                producto.save()
                #si cumple, se guarda en l bd con el método save de Django
                # form.save()
                #redirige a la lista de productos
                success_message = 'Producto creado exitosamente.'
                messages.success(request, success_message)                 

                return redirect('tienda_usuario')   
        else:
            print("ERRORES:", form.errors)# Imprime los errores del formulario en la consola para depuración
            # error_message = 'Error al crear el producto. Por favor, revise los datos ingresados.'
            # messages.error(request, error_message)

    #si el método es GET muestra el formulario vacío
    else:
        form = Form_producto()

    #se carga el formulario para crear el producto
    return render(request,'productos/crear_producto.html',{
        'form':form,
        'titulo':'Crear Producto'})
    
@login_required
def funcion_vista_previa(request, pk):
    producto = get_object_or_404(Producto, pk=pk, user=request.user)
    return render(request, 'productos/vista_previa.html', {'producto': producto})

@login_required
def confirmar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, user=request.user)
    producto.estado_producto = 'publicado'
    producto.save()

    messages.success(request, "Producto publicado correctamente.")
    return redirect('tienda_usuario')

@login_required
def cancelar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, user=request.user)
    # Solo permitir eliminar si es borrador
    if producto.estado_producto == 'borrador':
        producto.delete()

    messages.info(request, "Creación del producto cancelada.")

    return redirect('tienda_usuario')

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, user=request.user)
    print(request.POST)
    print(request.POST.get('accion'))

    if request.method == 'POST':
        form = Form_producto(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            print("FORMULARIO VALIDO")
            accion = request.POST.get('accion')
            producto = form.save()
            
            if accion == 'vista_previa':
                return redirect('vista_previa', producto.id)
            
            elif accion == 'cancelar':
                producto.delete()
                return redirect('tienda_usuario')
            
            elif accion == 'guardar':
                return redirect('tienda_usuario')
        else:
            print("FORMULARIO NO VALIDO")
            print(form.errors)
            # return redirect('vista_previa', producto.id)
    else:
        form = Form_producto(instance=producto)

    return render(request, 'productos/crear_producto.html', {'form': form})