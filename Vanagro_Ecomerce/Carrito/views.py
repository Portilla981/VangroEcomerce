# from pyexpat.errors import messages
from django.shortcuts import render

from django.shortcuts import render, redirect
# from django.http import HttpResponse
# Ruta para obtener las vistas genéricas de django para el CRUD

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# Esta ruta importa las vistas genéricas para crear, actualizar y eliminar elementos del modelo
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
# Ruta para manejar la autenticación y redireccionamiento
from django.urls import reverse_lazy
# Ruta para manejar el modelo de usuarios y login
from django.contrib.auth.views import LoginView
# Ruta para manejar la mezcla de autenticación en las vistas
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
# Importación del modelo Tarea creado
from .models import *
# from .form_home import *
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from Producto.models import Producto
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import ItemCarrito
from Pedido.models import Pedido, DetallePedido

# Create your views here.

# El usuario debe estar autenticado para ver el carrito
@login_required
#vista para ver el carrito
def ver_carrito(request):
    #busca los productos del carrito (que son seleccionados por el usuario)
    items = ItemCarrito.objects.filter(usuario=request.user)

    #se calcula el total por cada uno de los items(productos), por cada item hay un subtotal
    #el subtotal se calcula con el modelo (esta registrado en el modelo)
    total = sum(item.subtotal() for item in items)

    #se envía a la vista ver_carrito los productos y el total
    return render(request, 'carrito/ver_carrito.html', {'items': items, 'total': total, 'titulo': 'Mis compras'})

#------------------------------------------------------------------------------------------------
# El usuario debe estar autenticado para ver el carrito
@login_required
# vista para agregar al carrito
def agregar_al_carrito(request, producto_id):
    '''get_object_or_404 busca en la bd el producto que llega como ID por la URL. Si el producto 
    no existe muestra error 404'''
    producto = get_object_or_404(Producto, id=producto_id)

    # Validación
    #si el producto no esta activo o no tiene stock
    if not producto.activo or producto.stock <= 0:
        #mensaje del JS que el producto no se puede agregar
        return JsonResponse({"success": False, "error": "Este producto está agotado."})

    #se realiza una búsqueda en el carrito si el producto que se desea agregar ya esta en el carrito.
    #si el producto no esta en el carrito -> lo crea
    item, creado = ItemCarrito.objects.get_or_create(usuario=request.user, producto=producto)

    #si el producto esta en el carrito
    if not creado:
        #se valida el stock antes de sumar el producto
        if item.cantidad + 1 > producto.stock:
            #mensaje si lo solicitado supera el stock
            return JsonResponse({"success": False, "error": "No hay suficiente stock disponible."})
        #si no suma uno
        item.cantidad += 1
    #si el producto no estaba en el carrito suma 1
    else:
        item.cantidad = 1

    # guarda en la bd
    item.save()

    # suma la cantidad de productos (solo los registros sin tener en cuenta el valor)
    total_items = ItemCarrito.objects.filter(usuario=request.user).count()

    # el JS muestra que se agregó correctamente e indica el total de items (productos)
    return JsonResponse({"success": True, "total_items": total_items})

#------------------------------------------------------------------------------------------------

# el usuario debe estar autenticado para ver el carrito
@login_required
#vista para actualizar la cantidad
def actualizar_cantidad(request, item_id):

    #verifica que el usuario tenga el carrito con los productos de la bd. 
    #usuario=request.user -> evita que un usuario modifique el carrito de otro
    item = get_object_or_404(ItemCarrito, id = item_id, usuario=request.user)

    #cantidad del producto
    cantidad = int(request.POST.get("cantidad"))

    #cantidad negativa o cero
    if cantidad < 1:
        return JsonResponse({"success": False, "error": "Cantidad inválida"})

    #cantidad no sea mayor al stock
    if cantidad > item.producto.stock:
        return JsonResponse({"success": False, "error": "Stock insuficiente"})

    #actualiza la cantidad
    item.cantidad = cantidad
    #se guarda
    item.save()

    #se calcula el subtotal por cada producto
    subtotal = item.subtotal()

    #calcula el total del carrito (toma cada subtotal)
    total = sum(i.subtotal() for i in ItemCarrito.objects.filter(usuario=request.user))

    #mensaje con el subtotal de cada producto y el total del carrito. Informa que todo quedo ok
    return JsonResponse({"success": True, "subtotal": subtotal, "total": total})


#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------

# el usuario debe estar autenticado para ver el carrito
@login_required
#vista para eliminar un item (producto) del carrito
def eliminar_item(request, item_id):

    #obtiene los productos del carrito del usuario. 
    #usuario=request.user -> evita que un usuario modifique el carrito de otro
    item = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    #borra el item () del carrito
    item.delete()

    #calcula el total del carrito con el subtotal de los productos (Ajusta de acuerdo a los productos borrados)
    total = sum(i.subtotal() for i in ItemCarrito.objects.filter(usuario=request.user))
    #cuenta la nueva cantidad de items que tiene el carrito
    total_items = ItemCarrito.objects.filter(usuario=request.user).count()
    #mensaje con el nuevo total del carrito. Que la eliminación fue satisfactoria. Informa que todo quedo ok
    return JsonResponse({"success": True, "total": total, "total_items": total_items})

#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------

# el usuario debe estar autenticado para ver el carrito
@login_required
#vista para finalizar la compra(antes de pagar)
def finalizar_compra(request):

    #busca los producto en el carrito. Un usuario no puede modificar el carrito de otro
    items = ItemCarrito.objects.filter(usuario=request.user)

    #validación de que el carrito tenga productos
    if not items.exists():
        #si no encuentra productos en el carrito, redirige a ver_carrito
        return redirect('ver_carrito')
    #si el carrito esta vacío no puede continuar

    #Recorre todos los productos toma el subtotal y calcula el total
    total = sum(item.subtotal() for item in items)

    #carga finalizar_compra.html con los producto, el total y el usuario
    return render(request, 'carrito/finalizar_compra.html', {'items': items, 'total': total, 'usuario': request.user})

#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------

# el usuario debe estar autenticado para ver el carrito
@login_required
#requiere el método post (seguridad)
@require_POST
#guarda la transacción cuando este completa. Si no se completa no guarda
@transaction.atomic
#vista para procesar el pago
def procesar_pago(request):

    #se recibe el método de pago del formulario
    metodo_pago = request.POST.get("metodo_pago")

    #carga los productos que el usuario va a comprar
    items = ItemCarrito.objects.filter(usuario=request.user)

    #se valida que el carrito no se encuentre vació
    if not items.exists():
        #redirige a ver_carrito (no se puede pagar)
        return redirect('ver_carrito')

    total = 0

    # Validación de stock y calculo del total a pagar
    for item in items:
        #si la cantidad supera el stock
        if item.cantidad > item.producto.stock:
            #redirige a ver_carrito
            return redirect('ver_carrito')
        #sino realiza el calculo del subtotal por cada producto, para luego calcular el total
        total += item.subtotal()

    # Crear pedido en la bd (modelo pedidos). Gurda el usuario, el total y el estado del pedido
    pedido = Pedido.objects.create(usuario=request.user, total=total, estado='Pagado')

    # Ciclo para Crear detalles del pedido y descontar stock
    for item in items:
        #guarda el pedido, producto, cantidad y precio
        DetallePedido.objects.create(pedido=pedido, producto=item.producto, cantidad=item.cantidad, precio=item.producto.precio)
        #se descuenta del stock
        item.producto.stock -= item.cantidad
        #si el stock queda en 0
        if item.producto.stock == 0:
            #se desactiva de forma automática el producto
            item.producto.activo = False
        #guardamos
        item.producto.save()

    # Borra los productos del carrito
    items.delete()
    #compra exitosa e indica el id del pedido
    return redirect('pedido_exitoso', pedido_id=pedido.id)

#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------

# el usuario debe estar autenticado para ver el carrito
@login_required
def compra_exitosa(request):
    #redirige a compra_exitosa.html, una vez la compra es exitosa
    return render(request, 'carrito/compra_exitosa.html')