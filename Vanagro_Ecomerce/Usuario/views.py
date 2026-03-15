from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
from django.shortcuts import get_object_or_404

from Usuario.forms import UserForm, Formulario_Usuario, Formulario_Productor, Form_Actualizar_User
# Importación del modelo Tarea creado
from .models import *
# from .form_home import *
from django.contrib import messages
from django.db import transaction

# Create your views here.

class Login(DeleteView, LoginRequiredMixin):
    model = CreacionUsuario
    template_name = 'usuario/login.html'
    context_object_name = 'perfil'

    def get_object(self):
        #return self.request.user.creacionusuario
        perfil, created = CreacionUsuario.objects.get_or_create(user=self.request.user)
        return perfil
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['titulo']= 'Sesion de Usuario'        
        return context


class Tienda(TemplateView, LoginRequiredMixin):
    template_name = 'usuario/producter-profile.html'
    
    # success_message = 'Producto creado exitosamente.'
    # messages.success(request, success_message)   
    def dispatch(self, request, *args, **kwargs):
        # messages.info(request, 'Ingresando al módulo de tienda')
        return super().dispatch(request, *args, **kwargs)  

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context['titulo']= 'Tienda de Productos'
        
        return context
    

class RegistroUsuario(View):
    template_name = "usuario/registro.html"
    titulo = 'Registro de Usuario'

    def dispatch(self, request, *args, **kwargs):
        # messages.info(request, 'Ingresando al módulo de registro')
        return super().dispatch(request, *args, **kwargs)

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
        perfil_form = Formulario_Usuario(request.POST, request.FILES)
        perfil_form.fields['municipio'].queryset = Municipio.objects.all()        

        if user_form.is_valid() and perfil_form.is_valid():

            try:
                with transaction.atomic():
                    print("Formularios válidos. Procediendo a crear el usuario y perfil.")

                    # Crear usuario
                    usuario = User.objects.create_user(
                        first_name = user_form.cleaned_data['first_name'],
                        last_name = user_form.cleaned_data['last_name'],
                        username = user_form.cleaned_data['username'],    
                        email = user_form.cleaned_data['email'],
                        password = user_form.cleaned_data['password1']
                    )

                    CreacionUsuario.objects.create(
                        user=usuario,
                        departamento=perfil_form.cleaned_data['departamento'],  
                        municipio=perfil_form.cleaned_data['municipio'],
                        tipo_identificacion=perfil_form.cleaned_data['tipo_identificacion'],
                        numero_identificacion=perfil_form.cleaned_data['numero_identificacion'],
                        telefono_1=perfil_form.cleaned_data['telefono_1'],
                        telefono_2=perfil_form.cleaned_data['telefono_2'],
                        direccion_residencia=perfil_form.cleaned_data['direccion_residencia'],
                        fecha_nacimiento=perfil_form.cleaned_data['fecha_nacimiento'],
                        fotografia=perfil_form.cleaned_data['fotografia']
                    )
                    
                    print(f"Usuario {usuario.username} y perfil creado exitosamente.")

                    messages.success(request, f'Usuario {usuario.username} creado exitosamente.') 
                    return redirect("inicio_vista")
                
            except Exception as e:
                print("Error al crear el usuario o perfil:", e)
                messages.error(request, 'Ocurrió un error al crear el usuario. Por favor, inténtalo de nuevo.')
                return redirect("registro_usuario")
        
        messages.error(request, user_form.errors)
        messages.error(request, perfil_form.errors)
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


class RegistroProductor(TemplateView, LoginRequiredMixin):
    template_name = "usuario/tienda.html"

    def dispatch(self, request, *args, **kwargs):
        # messages.info(request, 'Ingresando al módulo de creación de tienda')
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)        

        user = self.request.user
        
        if hasattr(user, 'productor'):
            context['titulo']= 'Tu tienda'
            context['es_productor'] = True
            context['productor'] = user.productor
            context['perfil'] = CreacionUsuario.objects.get(user=user)

        else:
            context['titulo']= 'Registro de tienda'
            context['es_productor'] = False
            context['form'] = Formulario_Productor()
            context['form'].fields['municipio'].queryset = Municipio.objects.all()
        
        return context
    
    # POST → Guardar datos
    def post(self, request, *args, **kwargs):

        # Validación principal
        if hasattr(request.user, 'productor'):
            return redirect('tienda_usuario')  # ya existe

        form = Formulario_Productor(request.POST, request.FILES)

        if form.is_valid():
            productor = form.save(commit=False)
            productor.user = request.user
            productor.save()

            messages.success(request, f'La finca {productor.nombre_finca} ha sido creada exitosamente.') 

            return redirect('tienda_usuario')

        return self.render_to_response({'form': form})
    
    
    
@login_required
def editar_usuario(request):
    
    user = request.user
    perfil = request.user.usuario
    
    if request.method == 'POST':        
        user_form = Form_Actualizar_User(request.POST, instance = user)
        perfil_form = Formulario_Usuario(request.POST, request.FILES,  instance = perfil)
        
        if user_form.is_valid() and perfil_form.is_valid():            
            user_form.save()
            perfil_form.save()

            messages.success(request, f'El usuario {user.username} ha sido editado exitosamente.')            
            
            return redirect('sesion_inicio')
        
        if not user_form.is_valid():
            messages.success(request, user_form.errors) 
            print(user_form.errors)

        if not perfil_form.is_valid():
            messages.success(request, perfil_form.errors) 
            print(perfil_form.errors)   
        
    else:
        # messages.success(request, 'Ingresando al modulo de edición de usuario') 
        user_form = Form_Actualizar_User(instance= user)
        perfil_form = Formulario_Usuario(instance= perfil)
        
    context = {
        'user_form': user_form,
        'perfil_form': perfil_form,
        'titulo': 'Editar Usuario' 
        }
        
        
    return render(request, 'usuario/editar_usuario.html', context)