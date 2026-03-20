from django.urls import path

from django.contrib.auth.views import LogoutView # Ruta para manejar el cierre de sesion

from .views import * 

urlpatterns = [ 
    path('sesion/', Login.as_view(), name= 'sesion_inicio'),   
    path('tienda/', RegistroProductor.as_view(), name= 'tienda_usuario'),  
    path('salir/', LogoutView.as_view(next_page = 'inicio'), name='logout'),   
    path('registro/', RegistroUsuario.as_view(), name='registro_usuario'),
    path('editar/<int:pk>/', editar_usuario, name='editar_usuario'),
    path('editar/tienda/', EditarProductor.as_view() , name='editar_tienda'),
    path('lista/usuarios', ListaUsuarios.as_view(), name='lista_usuarios'),
    path('usuario/activo/<int:pk>/', toggle_usuario, name='accion_usuario'),
    path('ajax/Municipios/', cargar_municipios, name='lista_municipios'),
    # path("editar/imagen/", cambiar_imagen_usuario, name="actualizar_img"),   
]


