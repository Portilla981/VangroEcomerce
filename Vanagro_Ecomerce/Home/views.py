# from pyexpat.errors import messages
from django.shortcuts import render

from django.shortcuts import render, redirect
# from django.http import HttpResponse
# Ruta para obtener las vistas genéricas de django para el CRUD

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# Esta ruta importa las vistas genéricas para crear, actualizar y eliminar elementos del modelo
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
# Ruta para manejar la autenticación y redireccionamiento
from django.urls import reverse_lazy
# Ruta para manejar el modelo de usuarios y login
from django.contrib.auth.views import LoginView
# Ruta para manejar la mezcla de autenticación en las vistas
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Importación del modelo Tarea creado
from .models import *
from .form_home import *
from django.contrib import messages


# Create your views here.

class Home(TemplateView):
    template_name = 'home/nosotros.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['titulo']= 'Nosotros'
        
        context['cards']=[            
            {
                "title":"Nosotros",
                "description":"<strong>VANAGRO</strong><br> es un proyecto del SENA creado para conectar a los campesinos colombianos con los consumidores, promoviendo la compra directa, el comercio justo y el reconocimiento al trabajo del campo.",
                "img":"img/interfaz_vanagro/recolector.jpg"
            },
            {
                "title":"Misión",
                "description":"Ser la plataforma líder en Colombia en la conexión entre el campo y el consumidor, promoviendo un sistema agroalimentario más justo, sostenible y humano, en donde los productos campesinos sean valorados, visibles y preferidos por su calidad, origen y aporte al desarrollo rural.",
                "img":"img/interfaz_vanagro/vendefruta.jpg"
            },
            {
                "title":"Visión",
                "description":"Impulsar la comercialización directa de productos campesinos a través de una plataforma digital accesible, transparente y solidaria, que fomente el consumo consciente, fortalezca la economía rural y reconozca el esfuerzo de las comunidades colombianas.",
                "img":"img/products/caña.jpg"
            }
            ]        
        
        return context
    
    
class Contactenos(CreateView):    
    
    modelo = Mensaje
    
    form_class = Form_contacto
    
    template_name = 'home/contact-us.html'
    
    success_url = reverse_lazy('inicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['titulo']= 'Contactenos'
        
        return context
    
    def form_valid(self, form):
        # Aquí puedes realizar cualquier acción adicional antes de guardar el formulario
        # Por ejemplo, enviar un correo electrónico o registrar la información en otro modelo
        messages.error(self.request, '¡Gracias por contactarnos! Nos pondremos en contacto contigo pronto.')
        # Guardar el formulario y redirigir al usuario a la página de éxito
        return super().form_valid(form) 
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrige los errores en el formulario.')
        return super().form_invalid(form)
    

class Inicio(LoginView):
    template_name = 'home/inicio.html'
    modelo = User
    # success_url = reverse_lazy('inicio_vista')
    
    
    # Campos que se van a utilizar en el formulario de logueo
    fields = '__all__'  
    # Condicion para redireccionar si el usuario ya esta autenticado
    redirect_authenticated_user = True
    # Redireccion despues de iniciar sesion exitosamente
    def get_success_url(self):
        # Redireccion a la vista despues de iniciar sesion
        return reverse_lazy('sesion_inicio')  
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['titulo']= 'Inicio'
        
        return context

    
    

