from django import views
from django.urls import path

from django.contrib.auth.views import LogoutView # Ruta para manejar el cierre de sesion
# from . import views
from .views import * 

urlpatterns = [ 
    # path('Productos/', .as_view(), name= 'inicio'),   
    path('Crear/Producto/', crear_producto, name= 'crear_producto'),   
       
    
]
