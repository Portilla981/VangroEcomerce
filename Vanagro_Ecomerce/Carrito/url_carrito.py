from django.urls import path

from django.contrib.auth.views import LogoutView # Ruta para manejar el cierre de sesion
from django.contrib.auth import views as auth_views
from .views import * 

urlpatterns = [      
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_carrito'),
    path('actualizar/<int:item_id>/', actualizar_cantidad, name='actualizar_cantidad'),
    path('eliminar/<int:item_id>/', eliminar_item, name='eliminar_item'),
    path('finalizar/', finalizar_compra, name='finalizar_compra'),
    path('procesar/', procesar_pago, name='procesar_pago'),
	#path('exito/<int:pedido_id>/', views.pedido_exitoso, name='pedido_exitoso'),
]
