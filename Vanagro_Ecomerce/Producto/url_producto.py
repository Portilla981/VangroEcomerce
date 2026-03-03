from django import views
from django.urls import path

from django.contrib.auth.views import LogoutView # Ruta para manejar el cierre de sesion

from .views import * 

urlpatterns = [ 
    # path('Productos/', .as_view(), name= 'inicio'),   
    path('Crear/Producto/', crear_producto, name= 'crear_producto'),  
    path('Vista_previa/<int:pk>/', funcion_vista_previa, name='vista_previa'),

    path('Confirmar/<int:pk>/', confirmar_producto, name='guardar_producto'),

    path('editar/<int:pk>/', editar_producto, name='volver_crear'),

    path('cancelar/<int:pk>/', cancelar_producto, name='cancelar_producto'), 
       
    
]
