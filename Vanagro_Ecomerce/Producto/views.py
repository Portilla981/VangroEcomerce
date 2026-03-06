# from pyexpat.errors import messages
from django.contrib import messages

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import Form_producto
from .models import Producto
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils import timezone
from datetime import timedelta


# Create your views here.

def ver_productos(request):
    productos = Producto.objects.filter(
        estado_producto='publicado',
        activo=True,
        stock__gt=0
        ).select_related('productor', 'productor__user')
    
    print("Productos encontrados:", productos.count())

    return render(request, 'productos/vista_productos.html', {
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




class Listado_producto(LoginRequiredMixin, ListView):

    model = Producto
    template_name = "productos/listado_productos.html"
    context_object_name = "productos"

    def dispatch(self, request, *args, **kwargs):

        next_url = request.GET.get('next')
        if next_url:
            request.session['next'] = next_url

        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):        
        return Producto.objects.filter(productor__user=self.request.user)

def get_success_url(self):
    return self.request.POST.get('next', reverse_lazy('mis_productos'))


@login_required
#vista para actualizar el estado del producto de forma automatica (sin actualizar la pagina)
def toggle_producto(request, pk):

    if request.method == 'POST':
        '''get_object_or_404 busca en la bd el producto que llega como ID por la URL. Si el producto 
        no existe muestra error 404'''
        #Producto es el producto al que se le desea cambiar el estado
        producto = get_object_or_404(Producto, pk=pk, productor__user=request.user)
        #cambia el estado actual del producto  
        producto.activo = not producto.activo
        #utilizamos el método save de Django para actualizar el estado del producto
        producto.save()

        #indica si el cambio de estado fue realizado e indica el nuevo estado del producto
        return redirect(request.POST.get('next', 'mis_productos'))
    
    return redirect('mis_productos')



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

@login_required
def toggle_producto(request, pk):
    if request.method == "POST":
        producto = get_object_or_404(
            Producto,
            pk=pk,
            productor__user=request.user
        )
        producto.activo = not producto.activo
        producto.save()

        return redirect(request.POST.get('next', 'tienda_usuario'))

    return redirect('tienda_usuario')

#Vista para actualizar un producto, con la vista UpdateView que tiene Django
class Actualizar_producto(LoginRequiredMixin, UpdateView):
     #se trabaja con el model Producto para acceder a los campos
    model = Producto
    #utiliza el formulario ProductoForm que tiene forms
    form_class = Form_producto
    #archivo HTML que se usa para actualizar el producto
    template_name = 'productos/editar_producto.html'
    #después de guardar (lo hace la vista UpdateView) redirige a la vista lista de productos
    success_url = reverse_lazy('mis_productos')