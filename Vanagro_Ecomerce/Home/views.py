# from pyexpat.errors import messages
from django.shortcuts import render, redirect
# Ruta para obtener las vistas genéricas de django para el CRUD
from django.views.generic import TemplateView
# Esta ruta importa las vistas genéricas para crear, actualizar y eliminar elementos del modelo
from django.views.generic.edit import CreateView
# Ruta para manejar la autenticación y redireccionamiento
from django.urls import reverse_lazy
# Ruta para manejar el modelo de usuarios y login
from django.contrib.auth.views import LoginView
# Ruta para manejar la mezcla de autenticación en las vistas
from django.contrib.auth import logout
# Importación del modelo Tarea creado
from .models import *
from .form_home import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
class Home(TemplateView):
    template_name = 'home/nosotros.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['titulo']= 'Nosotros'
        
        context['cards']=[            
            {
                "title":"Nosotros",
                "description":"Vanagro busca conectar el campo risaraldense con la ciudad, facilitando el acceso directo a productos locales. Promueve el desarrollo rural, el consumo consciente y proyecta su crecimiento hacia todo el territorio colombiano.",
                "img":"img/interfaz_vanagro/vanagro4.jpg"
            },
            {
                "title":"Misión",
                "description":"Facilitar la conexión entre productores del campo risaraldense y consumidores urbanos mediante una plataforma accesible, promoviendo el comercio justo, la transparencia y el fortalecimiento de la economía local.",
                "img":"img/interfaz_vanagro/vanagro1a.jpg"
            },
            {
                "title":"Visión",
                "description":"Consolidarse como una plataforma referente en la integración del sector agrícola con la ciudad, iniciando en Risaralda y proyectándose a nivel nacional, destacándose por su impacto social y desarrollo sostenible.",
                "img":"img/interfaz_vanagro/vanagro3.jpg"
            }
            ]        
        
        return context
    
    
class Contactenos(CreateView):       
    model = Mensaje    
    form_class = Form_contacto    
    template_name = 'home/contact-us.html'    
    
    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('sesion_inicio')
        return reverse_lazy('inicio')
    
    # Autocompletar USUARIO
    def get_initial(self):
        initial = super().get_initial()

        if self.request.user.is_authenticated:
            user = self.request.user      
            initial['nombres'] = user.first_name
            initial['apellidos']= user.last_name
            initial['email']= user.email
            
            if hasattr(user, 'usuario'):
                initial['telefono'] = user.usuario.telefono_1

        return initial
    

    def form_valid(self, form):
        # Guardamos SIN confirmar aún
        mensaje = form.save(commit=False)
        user = self.request.user

        # Diferenciar tipo de mensaje
        if user.is_authenticated:
            mensaje.usuario = user
            mensaje.tipo = 'usuario'
        else:
            mensaje.tipo = 'publico'

        mensaje.save()

        # DATOS PARA EL CORREO
        asunto_msg = form.cleaned_data.get('asunto')
        nombre_completo = f"{form.cleaned_data.get('nombres')} {form.cleaned_data.get('apellidos')}"
        email_remitente = form.cleaned_data.get('email')
        telefono_remitente = form.cleaned_data.get('telefono')
        texto_mensaje = form.cleaned_data.get('mensaje')

        # ENVÍO DE CORREO
        try:                        
            asunto = f"Nuevo mensaje de contacto: {asunto_msg}"

            contenido = (
                f"Tipo: {mensaje.tipo}\n"
                f"Nombre: {nombre_completo}\n"
                f"Correo: {email_remitente}\n"
                f"Teléfono: {telefono_remitente}\n\n"
                f"Mensaje:\n{texto_mensaje}"
            )
            
            send_mail(
                asunto,
                contenido,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            messages.success(
                self.request,
                '¡Muchas gracias por su mensaje! En breve nos pondremos en contacto con usted.'
            )

        except Exception:
            messages.warning(
                self.request,
                'Su mensaje se ha recibido correctamente en nuestro sistema. Sin embargo, tuvimos un inconveniente al enviarle el correo de confirmación. No se preocupe, atenderemos su solicitud en breve.'
            )

        return super().form_valid(form)       


    # MANEJO DE ERRORES
    def form_invalid(self, form):
        error_msg = "Por favor corrija los siguientes campos en el formulario: "

        for field, errors in form.errors.items():
            nombre_limpio = field.replace('_', ' ').capitalize()
            error_msg += f"\n• {nombre_limpio}: {', '.join(errors)}"

        messages.error(self.request, error_msg)

        return super().form_invalid(form)
    

    # CONTEXTO
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['titulo'] = 'Contáctenos'        
        return context
    

class Inicio(LoginView):
    template_name = 'home/inicio.html'        
    # Condición para redireccionar si el usuario ya esta autenticado
    redirect_authenticated_user = True
    # Redireccion después de iniciar sesion exitosamente
    # def get_success_url(self):
    #     user = self.request.user
    #     if user.is_superuser:
    #         return reverse_lazy('sesion_inicio')

    #     # Redireccion a la vista después de iniciar sesion
    #     return reverse_lazy('sesion_inicio')  
    
    def get(self, request, *args, **kwargs):
        request.session.pop('usuario_inactivo', None)
        return super().get(request, *args, **kwargs)
       
    # si el usuario es valido 
    def form_valid(self, form):
        username = self.request.POST.get('username')
        user = form.get_user()
        if user.is_superuser:
            messages.success(self.request, f"Le damos la bienvenida, {username}. Ha ingresado al sistema con éxito.")
            return super().form_valid(form)

        perfil = user.usuario  

        if not user.is_active:
            messages.error(self.request,
                "Su usuario se encuentra desactivado. Por favor, comuníquese con soporte."
            )
            return self.form_invalid(form)               

        if not perfil.verificado:
            messages.error(
                self.request,
                "Su cuenta aún no ha sido activada. Por favor, revise su correo electrónico o solicite un nuevo enlace de activación."
            )

            self.request.session['usuario_inactivo'] = user.email
            return super().form_invalid(form)

        messages.success(self.request, f"Le damos la bienvenida, {username}. Ha ingresado al sistema con éxito.")
        return super().form_valid(form)
        

    # Si el usuario no es
    def form_invalid(self, form):
        username = self.request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            perfil = user.usuario  

            if not user.is_active:
                messages.error(
                    self.request,
                    "La cuenta se encuentra desctivada actualmente. Por favor, comuníquese con soporte."
                )
                return super().form_invalid(form)
            
            if not perfil.verificado:
                messages.error(
                    self.request,
                    "Su cuenta aún no ha sido activada. Por favor, revise su correo electrónico o solicite un nuevo enlace de activación."
                )

                self.request.session['usuario_inactivo'] = user.email

                return super().form_invalid(form)
            
            messages.error(self.request, "El usuario o la contraseña son incorrectos. Por favor, inténtelo de nuevo.")

        except User.DoesNotExist:
            messages.error(self.request, "El usuario o la contraseña son incorrectos. Por favor, inténtelo de nuevo.")

        return super().form_invalid(form)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Inicio'
        return context

    
def logout_view(request):
    logout(request)
    return redirect('inicio')