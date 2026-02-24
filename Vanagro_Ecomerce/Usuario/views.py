from django.http import JsonResponse
from django.shortcuts import render

from django.shortcuts import render, redirect
# from django.http import HttpResponse
# Ruta para obtener las vistas genéricas de django para el CRUD

from django.views.generic import TemplateView, View
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

from Usuario.forms import UserForm, Formulario_Usuario
# Importación del modelo Tarea creado
from .models import *
# from .form_home import *
from django.contrib import messages

# Create your views here.

class Login(TemplateView, LoginRequiredMixin):
    template_name = 'usuario/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['titulo']= 'Sesion de Usuario'
        
        return context


class Tienda(TemplateView, LoginRequiredMixin):
    template_name = 'usuario/producter-profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['titulo']= 'Tienda de Productos'
        
        return context
    
# class Registro(CreateView):
#     model = User
#     form_class = UserCreationForm
#     template_name = 'usuario/registro.html'
#     success_url = reverse_lazy('sesion_inicio')

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         username = form.cleaned_data.get('username')
#         messages.success(self.request, f'Usuario {username} creado exitosamente.')
#         return response
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         context['titulo']= 'Registro de Usuario'
        
#         return context

class RegistroUsuario(View):
    template_name = "usuario/registro.html"
    titulo = 'Registro de Usuario'

    def get(self, request):
        user_form = UserForm()
        perfil_form = Formulario_Usuario()
        
        return render(request, self.template_name, {
            "user_form": user_form,
            "perfil_form": perfil_form,
            "titulo": self.titulo
        })

    def post(self, request):
        user_form = UserForm(request.POST)
        perfil_form = Formulario_Usuario(request.POST)

        if user_form.is_valid() and perfil_form.is_valid():

            # Crear usuario
            user = User.objects.create_user(
                username=user_form.cleaned_data['username'],    
                email=user_form.cleaned_data['email'],
                password=user_form.cleaned_data['password1']
                )
            
            # user = user_form.save(commit=False)
            # user.set_password(user_form.cleaned_data['password'])
            # user.save()

            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()

            messages.success(request, f'Usuario {user.username} creado exitosamente.') 
            return redirect("sesion_inicio")
        
        messages.error(request, 'Error al crear el usuario. Por favor, revise los datos ingresados.') 
        
        print(user_form.errors)
        print(perfil_form.errors)


        return render(request, self.template_name, {
            "user_form": user_form,
            "perfil_form": perfil_form,
            "titulo": self.titulo
        })
    

def cargar_municipios(request):
        departamento_id = request.GET.get("departamento_id")
        municipios = Municipio.objects.filter(departamento_id=departamento_id)
        data = list(municipios.values("id", "nombre_Municipio"))
        return JsonResponse(data, safe=False)
