from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pedido


# Create your views here.
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

#Vista para pedido exitoso
#el usuario debe estar autenticado para crear el producto
@login_required
def pedido_exitoso(request, pedido_id):
    '''get_object_or_404 busca en la bd el pedido que llega como ID por la URL. Si el pedido 
    no existe muestra error 404'''
    #pedido del usuario logueado
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    #carga el HTML pedido_exitoso
    return render(request, 'pedidos/pedido_exitoso.html', {'pedido': pedido})


# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

#vista para los pedidos del usuario
#el usuario debe estar autenticado para crear el producto
@login_required
def mis_pedidos(request):
    #trae los pedidos que son del usuario logueado y los ordena por fecha
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    #carga el HTML de mis_pedidos
    return render(request, 'pedidos/mis_pedidos.html', {'pedidos': pedidos})


# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

#Vista para el detalle del pedido
#el usuario debe estar autenticado para crear el producto
@login_required
def detalle_pedido(request, pedido_id):
    '''get_object_or_404 busca en la bd el pedido que llega como ID por la URL. Si el pedido 
    no existe muestra error 404'''
    #pedido del usuario logueado
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    #carga el HTML de detalle_pedido
    return render(request, 'pedidos/detalle_pedido.html', {'pedido': pedido})