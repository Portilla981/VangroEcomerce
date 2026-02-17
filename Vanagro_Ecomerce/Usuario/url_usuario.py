from django.urls import path

from django.contrib.auth.views import LogoutView # Ruta para manejar el cierre de sesion
# from . import views
from .views import * 

urlpatterns = [ 
    path('Sesion', Usuario.as_view(), name= 'sesion_inicio'),   
    # path('Contactar/', Contactenos.as_view(), name= 'contactenos'),   
    # path('Inicio/', Inicio.as_view(), name= 'inicio_vista'),   
    
]
