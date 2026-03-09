from django.urls import path

from django.contrib.auth.views import LogoutView # Ruta para manejar el cierre de sesion
# from . import views
from .views import * 

urlpatterns = [ 
    path('sesion/', Login.as_view(), name= 'sesion_inicio'),   
    path('tienda/', RegistroProductor.as_view(), name= 'tienda_usuario'),  
    path('salir/', LogoutView.as_view(next_page = 'inicio'), name='logout'),   
    path('registro/', RegistroUsuario.as_view(), name='registro_usuario'),
    path('ajax/Municipios/', cargar_municipios, name='lista_municipios'),
]
