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

def lista_productos(request):
    productos = Producto.objects.filter(
        estado_producto='publicado',
        activo=True,
        stock__gt=0
        ).select_related('productor', 'productor__user')
    
    print("Productos encontrados:", productos.count())

    return render(request, 'productos/lista_productos.html', {
        'productos': productos
    })


def detalle_producto(request, pk):
    producto = get_object_or_404(
        Producto,
        pk=pk,
        estado_producto='publicado',
        activo=True,
        stock__gt=0
    )

    return render(request, 'productos/producto_detallado.html', {
        'producto': producto
    })




#el usuario debe estar autenticado para crear el producto
@login_required
# Vista para crear el producto
def crear_producto(request):

    # Eliminar borradores viejos del usuario
    tiempo_limite = timezone.now() - timedelta(minutes=15)

    Producto.objects.filter(
        productor =request.user.productor,
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
            producto.productor = request.user.productor  # Asignar el productor desde el usuario
            
            # Si quiere vista previa
            if accion == 'vista_previa':
                
                producto.estado_producto = 'borrador'
                producto.save()
                
                print(producto.imagen_producto)
                
                return redirect('vista_previa', producto.id)
            
            # Si quiere guardar directo
            elif accion == 'guardar':
                producto.estado_producto = 'publicado'
                producto.save()
                #si cumple, se guarda en l bd con el método save de Django
                #redirige a la lista de productos
                success_message = 'Producto creado exitosamente.'
                messages.success(request, success_message)                 

                return redirect('tienda_usuario')  

            elif accion == 'cancelar':
                return redirect('tienda_usuario') 
            
        else:
            print("ERRORES:", form.errors)
            # Imprime los errores del formulario en la consola para depuración
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
    producto = get_object_or_404(Producto, pk=pk, productor =request.user.productor)
    return render(request, 'productos/vista_previa.html', {'producto': producto})

@login_required
def confirmar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, productor=request.user.productor)
    producto.estado_producto = 'publicado'
    producto.activo = True
    producto.save()

    messages.success(request, "Producto publicado correctamente.")
    return redirect('tienda_usuario')

@login_required
def cancelar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, productor=request.user.productor)
    # Solo permitir eliminar si es borrador
    if producto.estado_producto == 'borrador':
        producto.delete()

    messages.info(request, "Creación del producto cancelada.")

    return redirect('tienda_usuario')

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, productor=request.user.productor)
    print(request.POST)
    print(request.POST.get('accion'))

    if request.method == 'POST':
        form = Form_producto(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            print("FORMULARIO VALIDO")
            accion = request.POST.get('accion')
            producto = form.save(commit=False)
            producto.productor = request.user.productor  # Asignar el productor desde el usuario
            
            if accion == 'vista_previa':
                producto.estado_producto = 'borrador'
                producto.save()
                return redirect('vista_previa', producto.id)
            
            elif accion == 'guardar':
                producto.estado_producto = 'publicado'
                producto.save()
                messages.success(request, "Producto actualizado correctamente.")
                return redirect('tienda_usuario')

            elif accion == 'cancelar':
                # 🔥 NO borrar si ya estaba publicado
                if producto.estado_producto == 'borrador':
                    producto.delete()
                return redirect('tienda_usuario')
        else:
            print("FORMULARIO NO VALIDO")
            print(form.errors)
            # return redirect('vista_previa', producto.id)
    else:
        form = Form_producto(instance=producto)

    return render(request, 'productos/crear_producto.html', {'form': form})