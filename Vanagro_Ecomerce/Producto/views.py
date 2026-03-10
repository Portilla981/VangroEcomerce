# from pyexpat.errors import messages
from django.contrib import messages

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import Form_producto
from .models import Producto
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView, FormView
from django.views import View
from django.urls import reverse, reverse_lazy
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

    
'''    
class Listado_producto(LoginRequiredMixin, ListView):
    model = Producto
    template_name = "productos/listado_productos.html"
    context_object_name = "productos"

    def get_queryset(self):        
        return Producto.objects.filter(productor__user=self.request.user)'''

def get_success_url(self):
    return self.request.POST.get('next', reverse_lazy('mis_productos'))






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
                
                url = reverse('vista_previa', args=[producto.id])
                
                return redirect(f"{url}?modo=crear")
                
                # return redirect('vista_previa', producto.id)
            
            elif accion == 'guardar':
                producto.estado_producto = 'publicado'
                producto.save()
                messages.success(request, "Producto actualizado correctamente.")
                return redirect('tienda_usuario')

            elif accion == 'cancelar':
                # NO borrar si ya estaba publicado
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





# Listar producto

class ListaProductos(LoginRequiredMixin, ListView):
    model = Producto
    template_name = "productos/listado_productos.html"
    context_object_name = "productos"
    
    # Accion para volvel a la pagina de donde se llamo
    def dispatch(self, request, *args, **kwargs):
        next_url = request.GET.get('next')

        if next_url:
            request.session['volver_a'] = next_url

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Producto.objects.filter(
            productor=self.request.user.productor
        )
        
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
                
                url = reverse('vista_previa', args=[producto.id])
                
                return redirect(f"{url}?modo=crear")
            
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

'''
# Crear producto
class CrearProducto(LoginRequiredMixin, FormView):

    template_name = "productos/crear_producto.html"
    # Método 1
    # form_class = Form_producto
    
    # def get_queryset(self):
    #	return Producto.objects.filter(productor=self.request.user.productor)

    # def form_valid(self, form):

    #     self.request.session["producto_data"] = self.request.POST
    #     self.request.session["producto_files"] = self.request.FILES

    #     return redirect("preview_producto")

    # Método 2
    def get(self, request):
        form = Form_producto()
        return render(request, self.template_name, {
            "form": form
        })

    def post(self, request):
        form = Form_producto(request.POST, request.FILES)
        accion = request.POST.get("accion")

        if form.is_valid():
            if accion == "vista_previa":
                producto = form.save(commit=False)

                return render(request, "productos/vista_previa.html", {
                    "producto": producto,
                    "form": form,
                    "modo": "crear"
                })

            elif accion == "guardar":
                producto = form.save(commit=False)
                producto.productor = request.user.productor
                producto.estado_producto = "publicado"
                producto.activo = True
                producto.save()

                return redirect("tienda_usuario")
        else:
            return redirect("tienda_usuario")

        return render(request, self.template_name, {"form": form})'''


@login_required
#vista para actualizar el estado del producto de forma automática (sin actualizar la pagina)
def toggle_producto(request, pk):

    if request.method == 'POST':
        #get_object_or_404 busca en la bd el producto que llega como ID por la URL. Si el producto no existe muestra error 404'''
        #Producto es el producto al que se le desea cambiar el estado
        producto = get_object_or_404(Producto, pk=pk, productor__user=request.user)
        #cambia el estado actual del producto  
        producto.activo = not producto.activo
        #utilizamos el método save de Django para actualizar el estado del producto
        producto.save()

        #indica si el cambio de estado fue realizado e indica el nuevo estado del producto
        return redirect(request.POST.get('next', 'mis_productos'))
    
    return redirect('mis_productos')



@login_required
def funcion_vista_previa(request, pk):
    producto = get_object_or_404(Producto, pk=pk, productor =request.user.productor)
    modo = request.GET.get('modo')

    return render(request, 'productos/vista_previa.html', {'producto': producto, 'modo': modo})

'''
# vista previa 
class PreviewProducto(LoginRequiredMixin, View):

    template_name = "productos/vista_previa.html"
    
    # def get_queryset(self):
	#     return Producto.objects.filter(productor=self.request.user.productor)
    
    def get(self, request):
        data = request.session.get("producto_data")

        form = Form_producto(data)

        producto = form.save(commit=False)

        return render(
            request,
            self.template_name,
            {
                "producto": producto,
                "form": form
            }
        )'''

# Guardar producto
class GuardarProducto(LoginRequiredMixin, View):

    # def get_queryset(self):
    # 	return Producto.objects.filter(productor=self.request.user.productor)

    def post(self, request):

        data = request.session.get("producto_data")

        files = request.session.get("producto_files")

        form = Form_producto(data, files)

        if form.is_valid():

            producto = form.save(commit=False)

            producto.productor = request.user.productor

            producto.save()

        request.session.pop("producto_data", None)
        request.session.pop("producto_files", None)

        return redirect("mis_productos")

# Editar producto
class EditarProducto(LoginRequiredMixin, View):

    template_name = "productos/editar_producto.html"
    
    # Método 1
    # model = Producto
    # form_class = Form_producto
       
    # def get_queryset(self):
    #     return Producto.objects.filter(
    #         productor=self.request.user.productor
    #     )

    # def form_valid(self, form):

    #     self.request.session["producto_data"] = self.request.POST
    #     self.request.session["producto_files"] = self.request.FILES
    #     self.request.session["producto_id"] = self.object.id

    #     return redirect("preview_producto")

    # Método 2
    def get(self, request, pk):

        producto = get_object_or_404(
            Producto,
            pk=pk,
            productor=request.user.productor
        )

        form = Form_producto(instance=producto)

        return render(request, self.template_name, {
            "form": form,
            "producto": producto,
            "modo": "editar"
        })

    def post(self, request, pk):

        producto = get_object_or_404(
            Producto,
            pk=pk,
            productor=request.user.productor
        )

        form = Form_producto(
            request.POST,
            request.FILES,
            instance=producto
        )

        accion = request.POST.get("accion")

        if form.is_valid():

            if accion == "vista_previa":

                producto_preview = form.save(commit=False)

                return render(
                    request,
                    "productos/vista_previa.html",
                    {
                        "producto": producto_preview,
                        "form": form,
                        "modo": "editar",
                        "pk": pk
                    }
                )

            if accion == "guardar":

                producto = form.save(commit=False)
                producto.productor = request.user.productor
                producto.estado_producto = "publicado"
                producto.activo = True
                producto.save()

                # form.save()

                return redirect("mis_productos")

        return render(request, self.template_name, {"form": form})



# Guardar edición
class GuardarProducto(LoginRequiredMixin, View):

    # def get_queryset(self):
	#     return Producto.objects.filter(productor=self.request.user.productor)

    def post(self, request):

        data = request.session.get("producto_data")
        files = request.session.get("producto_files")

        producto_id = request.session.get("producto_id")

        if producto_id:

            producto = Producto.objects.get(pk=producto_id)

            form = Form_producto(data, files, instance=producto)

        else:

            form = Form_producto(data, files)

        if form.is_valid():

            producto = form.save(commit=False)

            producto.productor = request.user.productor

            producto.save()

        request.session.flush()

        return redirect("mis_productos")
