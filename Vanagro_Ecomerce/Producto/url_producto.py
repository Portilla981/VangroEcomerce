
from django.urls import path

from django.contrib.auth.views import LogoutView # Ruta para manejar el cierre de sesion

from .views import * 

urlpatterns = [

    path("mis_productos/", ListaProductos.as_view(), name="mis_productos"),
    path("editar/imagen-producto/", cambiar_imagen_producto, name="actualizar_img"),
    
    # path('Mis_Productos/', Listado_producto.as_view(), name='mis_productos'),
    #path("productos/crear/", CrearProducto.as_view(), name="crear_producto"),
    path('crear/producto/', crear_producto, name= 'crear_producto'),  
    # path("productos/preview/", PreviewProducto.as_view(), name="preview_producto"),
    path('Vista_previa/<int:pk>/', funcion_vista_previa, name='vista_previa'),
    path("productos/guardar/", GuardarProducto.as_view(), name="guardar_producto"),
    path("productos/editado/", GuardarProductoEditado.as_view(), name="guardar_editado"),
    path('Confirmar/<int:pk>/', confirmar_producto, name='guardar_producto'),
    path("productos/<int:pk>/editar/", EditarProducto.as_view(), name="editar_producto"),
    path('editar/<int:pk>/', editar_producto, name='volver_crear'),
    path('productos/cards', ver_productos, name='ver_productos'), 
    # path('Productos', ver_productos, name='ver_productos'), 
    path('producto/<int:pk>/', detalle_producto, name='detalle_producto'),
    # path('Producto/<int:pk>/', detalle_producto, name='detalle_producto'),    
    path('Producto_Activo/<int:pk>/', toggle_producto, name='accion_producto'),
    # path('Producto_Activo/<int:pk>/', toggle_producto, name='accion_producto'),

    path('cancelar/<int:pk>/', cancelar_producto, name='cancelar_producto'), 
    
    #path("productos/<int:pk>/eliminar/", EliminarProducto.as_view(), name="eliminar_producto"),
    
    
    
    
    
    
    
    
    
    

]
