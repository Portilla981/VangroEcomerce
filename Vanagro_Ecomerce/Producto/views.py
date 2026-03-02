from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ProductoForm
from .models import Producto
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db import transaction

# Create your views here.

#el usuario debe estar autenticado para crear el producto
@login_required
# Vista para crear el producto
def crear_producto(request):

    #procesar el formulario (Si se envía)
    if request.method == 'POST':
        #Se capturan los datos del producto y la imagen
        form = ProductoForm(request.POST, request.FILES)

        #se valida si el formulario es valido
        if form.is_valid():
            #si cumple, se guarda en l bd con el método save de Django
            form.save()
            #redirige a la lista de productos
            return redirect('Usuario/tienda_usuario')

    #si el metodo es GET muestra el formulario vacío
    else:
        form = ProductoForm()

    #se carga el formulario para crear el producto
    return render(request,'productos/crear_producto.html',{'form':form})
