
from django.urls import path

from django.contrib.auth.views import LogoutView # Ruta para manejar el cierre de sesion

from .views import * 

urlpatterns = [ 
    # path('Productos/', .as_view(), name= 'inicio'),   
    path('Crear/Producto/', crear_producto, name= 'crear_producto'),  
    path('Vista_previa/<int:pk>/', funcion_vista_previa, name='vista_previa'),
    path('Confirmar/<int:pk>/', confirmar_producto, name='guardar_producto'),
    path('Editar/<int:pk>/', editar_producto, name='volver_crear'),
    path('Cancelar/<int:pk>/', cancelar_producto, name='cancelar_producto'), 
    path('Productos', ver_productos, name='ver_productos'), 
    path('Producto/<int:pk>/', detalle_producto, name='detalle_producto'),
    path('Mis_Productos/', Listado_producto.as_view(), name='mis_productos'),
    path('Producto_Activo/<int:pk>/', toggle_producto, name='accion_producto'),
    path('Editar_producto/<int:pk>/', Actualizar_producto.as_view(), name='editar_producto'),
]
