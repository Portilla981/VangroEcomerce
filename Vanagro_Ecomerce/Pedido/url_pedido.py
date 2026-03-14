from django.urls import path
from . import views

urlpatterns = [
    path('exitoso/<int:pedido_id>/', views.pedido_exitoso, name='pedido_exitoso'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('detalle/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
]