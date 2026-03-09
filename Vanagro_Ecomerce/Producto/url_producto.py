
from django.urls import path

from django.contrib.auth.views import LogoutView # Ruta para manejar el cierre de sesion

from .views import * 

urlpatterns = [

    path("productos/", ListaProductos.as_view(), name="mis_productos"),

    path("productos/crear/", CrearProducto.as_view(), name="crear_producto"),

    path("productos/preview/", PreviewProducto.as_view(), name="preview_producto"),

    path("productos/guardar/", GuardarProducto.as_view(), name="guardar_producto"),

    path("productos/<int:pk>/editar/", EditarProducto.as_view(), name="editar_producto"),

    path('productos/cards', ver_productos, name='ver_productos'), 
    path('producto/<int:pk>/', detalle_producto, name='detalle_producto'),
    path('Producto_Activo/<int:pk>/', toggle_producto, name='accion_producto'),

    #path("productos/<int:pk>/eliminar/", EliminarProducto.as_view(), name="eliminar_producto"),

]
