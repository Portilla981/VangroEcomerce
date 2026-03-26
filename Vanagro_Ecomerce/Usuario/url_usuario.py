from django.urls import path

from django.contrib.auth.views import LogoutView # Ruta para manejar el cierre de sesion

from .views import * 

urlpatterns = [ 
    path('sesion/', PerfilUsuario.as_view(), name= 'sesion_inicio'),   
    path('tienda/', RegistroProductor.as_view(), name= 'tienda_usuario'),  
    path('salir/', LogoutView.as_view(next_page = 'inicio'), name='logout'),   
    path('registro/', RegistroUsuario.as_view(), name='registro_usuario'),
    path('editar/usuario/<int:pk>/', editar_usuario, name='editar_usuario'),
    path('editar/tienda/<int:pk>/', EditarProductor.as_view() , name='editar_tienda'),
    path('tienda/gestion/', panel_ventas_productor, name='gestion_ventas'),
    path('tienda/gestion/<int:pk>', despachar_item, name='despachar'),
    path('informe', informe_ventas_productor, name='informe_ventas'),
    path('lista/usuarios', ListaUsuarios.as_view(), name='lista_usuarios'),
    path('mensajes', ListaMensajes.as_view(), name='mensajes_admin'),
    path('mensajes/respuesta', responder_mensaje, name='respuesta_msj'),
    path('usuario/activo/<int:pk>/', toggle_usuario, name='accion_usuario'),
    path('tienda/activo/', toggle_productor, name='accion_tienda'),
    path('ajax/Municipios/', cargar_municipios, name='lista_municipios'),
    # path("editar/imagen/", cambiar_imagen_usuario, name="actualizar_img"),   
]


