from django.shortcuts import render

from django.shortcuts import render, redirect
# from django.http import HttpResponse
# Ruta para obtener las vistas genericas de django para el CRUD

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# Esta ruta importa las vistas genericas para crear, actualizar y eliminar elementos del modelo
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
# Ruta para manejar la autenticacion y redireccionamiento
from django.urls import reverse_lazy
# Ruta para manejar el modelo de usuarios y login
from django.contrib.auth.views import LoginView
# Ruta para manejar la mezcla de autenticacion en las vistas
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Importacion del modelo Tarea creado
from .models import *


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
                "img":"img/vanagro/recolector.jpg"
            },
            {
                "title":"Misión",
                "description":"Ser la plataforma líder en Colombia en la conexión entre el campo y el consumidor, promoviendo un sistema agroalimentario más justo, sostenible y humano, en donde los productos campesinos sean valorados, visibles y preferidos por su calidad, origen y aporte al desarrollo rural.",
                "img":"img/vanagro/vendefruta.jpg"
            },
            {
                "title":"Visión",
                "description":"Impulsar la comercialización directa de productos campesinos a través de una plataforma digital accesible, transparente y solidaria, que fomente el consumo consciente, fortalezca la economía rural y reconozca el esfuerzo de las comunidades colombianas.",
                "img":"img/products/caña.jpg"
            }
            ]        
        
        return context
    
    
    

