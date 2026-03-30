from django.urls import path

from django.contrib.auth.views import LogoutView # Ruta para manejar el cierre de sesion
from django.contrib.auth import views as auth_views
from .views import * 

urlpatterns = [ 
    path('', Home.as_view(), name= 'inicio'),   
    path('Contactar/', Contactenos.as_view(), name= 'contactenos'),   
    path('Inicio/', Inicio.as_view(), name= 'inicio_vista'),
    path('Salir/', logout_view, name= 'salir'), 
    # Rutas para la recuperacion de contraseña
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),     
]
