"""
URL configuration for Vanagro_Ecomerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# Linea para incluir las rutas de las aplicaciones Home y Usuario
from django.urls import path, include
# Linea para manejar las rutas de archivos multimedia (imágenes, documentos, etc.) durante el desarrollo, esto permite servir los archivos almacenados en MEDIA_ROOT a través de MEDIA_URL.
# No olvide instalar Pillow para manejar las imágenes en Django, esto es necesario para trabajar con campos de imagen en los modelos y para procesar imágenes en el proyecto.
from django.conf import settings
from django.conf.urls.static import static

#from Vanagro_Ecomerce import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.url_home')), 
    path('', include('Usuario.url_usuario')),
    path('', include('Producto.url_producto')),
    path('', include('Carrito.url_carrito')),
    path('', include('Pedido.url_pedido')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Se incluyen las rutas de las aplicaciones Home y Usuario para que estén disponibles en el proyecto, esto permite organizar las URLs de cada aplicación de manera modular y facilita la gestión de las rutas en el proyecto.
