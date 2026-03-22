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

class PerfilUsuario(LoginRequiredMixin, DeleteView):
    model = CreacionUsuario
    template_name = 'usuario/login.html'
    context_object_name = 'perfil'

    def dispatch(self, request, *args, **kwargs):
        # Si es superusuario, lo dejamos entrar pero SIN perfil
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Si NO tiene perfil, mostramos mensaje y redirigimos
        if not hasattr(request.user, 'usuario'):
            messages.error(request, "No tienes perfil creado.")
            return redirect('inicio')  # ajusta esta ruta

        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        # Verifica si es superuser
        if self.request.user.is_superuser:
            return None

        #return self.request.user.creacionusuario
        return get_object_or_404(CreacionUsuario, user=self.request.user)
        # perfil, created = CreacionUsuario.objects.get_or_create(user=self.request.user)
        # return perfil
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['titulo']= 'Sesion de Usuario'  
        context['es_superuser'] = self.request.user.is_superuser      
        return context


class Tienda(LoginRequiredMixin, TemplateView):
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

        if 'cancelar-registro' in request.POST:
            messages.info(request, 'Saliendo sin guardar cambios')
            return redirect("inicio_vista")

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
                return render(request, self.template_name, {
                    "user_form": user_form,
                    "perfil_form": perfil_form,
                    "titulo": self.titulo
                    })
        
        else:

            # 1. Creamos una cadena de texto vacía
            error_msg = "Por favor corrige lo siguiente: "
    
            # 2. Recorremos ambos formularios
            for f in [user_form, perfil_form]:
                for field, errors in f.errors.items():
                    # Limpiamos el nombre del campo (ej: 'fecha_nacimiento' -> 'Fecha nacimiento')
                    nombre_limpio = field.replace('_', ' ').capitalize()
                    # Concatenamos: "Campo: error1, error2. "
                    error_msg += f"\n• {nombre_limpio}: {', '.join(errors)}. "

            # 3. Enviamos un ÚNICO mensaje de error al popup
            messages.error(request, error_msg)
     

            print(user_form.errors)
            print(perfil_form.errors)

            # for formulario in [form_user, form_perfil]:
            #     for field, errors in formulario.errors.items():
            #         for error in errors:
            #             # Enviamos cada error al sistema de mensajes
            #             nombre_campo = field.replace('_', ' ').capitalize()
            #             messages.error(request, f"{nombre_campo}: {error}")


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


class RegistroProductor(LoginRequiredMixin, TemplateView):
    template_name = "usuario/tienda.html"

    def dispatch(self, request, *args, **kwargs):
        # messages.info(request, 'Ingresando al módulo de creación de tienda')
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)        

        user = self.request.user

        # verifica si el usuario tiene productor
        if hasattr(user, 'productor'):
            context['titulo']= 'Tu tienda'
            context['es_productor'] = True
            context['productor'] = user.productor
            # context['perfil'] = CreacionUsuario.objects.get(user=user)
            context['perfil'], _ = CreacionUsuario.objects.get_or_create(user=user)

        else:
            form = Formulario_Productor()
            form.fields['municipio'].queryset = Municipio.objects.all()

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
        
        
        # 1. Creamos una cadena de texto vacía
        error_msg = "Por favor corrige lo siguiente: "

        # 2. Recorremos formularios
        for field, errors in form.errors.items():
            nombre_limpio = field.replace('_', ' ').capitalize()
            error_msg += f"\n• {nombre_limpio}: {', '.join(errors)}."

        # 3. Enviamos un ÚNICO mensaje de error al popup
        messages.error(request, error_msg)

        return render(request, self.template_name, {
            "form": form,
            "titulo": 'Registro de tienda',
            "es_productor": False
        })
    
    
@login_required
def editar_usuario(request, pk):
    
    # Buscamos el usuario por su ID
    perfil = get_object_or_404(CreacionUsuario, pk=pk)
    user = perfil.user # Accedemos al User de Django relacionado

    # Seguridad
    if perfil.user != request.user:
        return redirect('sesion_inicio')
        
    if request.method == 'POST':        
        user_form = Form_Actualizar_User(request.POST, instance = user)
        perfil_form = Formulario_Usuario(request.POST, request.FILES,  instance = perfil)
        
        if user_form.is_valid() and perfil_form.is_valid():            
            user_form.save()
            perfil_form.save()

            messages.success(request, f'El usuario {user.username} ha sido editado exitosamente.')            
            
            return redirect('sesion_inicio')
        
    
        # 1. Creamos una cadena de texto vacía
        error_msg = "Por favor corrige lo siguiente: "
        print(user_form.errors)
        print(perfil_form.errors) 

        # 2. Recorremos ambos formularios
        for f in [user_form, perfil_form]:
            for field, errors in f.errors.items():
                # Limpiamos el nombre del campo (ej: 'fecha_nacimiento' -> 'Fecha nacimiento')
                nombre_limpio = field.replace('_', ' ').capitalize()
                # Concatenamos: "Campo: error1, error2. "
                error_msg += f"\n• {nombre_limpio}: {', '.join(errors)}. "

        # 3. Enviamos un ÚNICO mensaje de error al popup
        messages.error(request, error_msg)    
        
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



class EditarProductor(LoginRequiredMixin, UpdateView):
    model = CreacionProductor 
    form_class = Formulario_Productor
    template_name = "usuario/editar_tienda.html"
    
    def get_object(self, queryset=None):
        # Si es superusuario → puede editar cualquiera
        if self.request.user.is_superuser:
            return get_object_or_404(CreacionProductor, pk=self.kwargs.get('pk'))

        # Esto asegura que el usuario SOLO edite su propio perfil de productor
        # y no el de otros, incluso si conoce el ID.
        return self.request.user.productor
    
    def get_success_url(self):
        # Lógica dinámica de redirección
        if self.request.user.is_superuser:
            return reverse_lazy('lista_usuarios') # Nombre de tu URL de la tabla
        return reverse_lazy('sesion_inicio') # URL para el productor normal

    def form_valid(self, form):
        messages.success(self.request, "Los datos de tu tienda han sido actualizados.")
        return super().form_valid(form)


    def form_invalid(self, form):
        error_msg = "Por favor corrige lo siguiente: "

        for field, errors in form.errors.items():
            nombre_limpio = field.replace('_', ' ').capitalize()
            error_msg += f"\n• {nombre_limpio}: {', '.join(errors)}. "

        messages.error(self.request, error_msg)

        return super().form_invalid(form)




class ListaUsuarios(LoginRequiredMixin, ListView):
    
    model = CreacionUsuario
    template_name = "usuario/listado_usuarios.html"
    context_object_name = "usuarios"     
        
    # Accion para volver a la pagina de donde se llamo
    def dispatch(self, request, *args, **kwargs):
        next_url = request.GET.get('next')

        if next_url:
            request.session['volver_a'] = next_url

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self): 

        usuarios = CreacionUsuario.objects.exclude(user__is_superuser=True).select_related('user__productor')

        for u in usuarios:
            u.es_productor = hasattr(u.user, 'productor')  # CLAVE

        return usuarios




@login_required
#vista para actualizar el estado del producto de forma automática (sin actualizar la pagina)
def toggle_usuario(request, pk):

    next_url = request.GET.get('next')

    if next_url:
        request.session['volver_a'] = next_url

    if request.method == 'POST'and request.user.is_superuser:
        #get_object_or_404 busca en la bd el producto que llega como ID por la URL. Si el producto no existe muestra error 404'''
        #Producto es el producto al que se le desea cambiar el estado
        tipo = request.POST.get('tipo') # verifica que tipo de dato esta recibiendo o a quien se debe modificar

        usuario = get_object_or_404(User, pk=pk)


        
        if usuario == request.user:
            return redirect('lista_usuarios')        
        
        # Accion para usuario
        if tipo == 'usuario':
            # perfil = usuario.user    
            #cambia el estado actual del producto  
            usuario.is_active = not usuario.is_active
            #utilizamos el método save de Django para actualizar el estado del producto
            usuario.save()

        elif tipo == 'productor':
            if hasattr(usuario, 'productor'):
                productor = usuario.productor
                productor.activo = not productor.activo
                productor.save()

        #indica si el cambio de estado fue realizado e indica el nuevo estado del producto
        return redirect(request.POST.get('next', 'lista_usuarios'))
    
    return redirect('lista_usuarios')
