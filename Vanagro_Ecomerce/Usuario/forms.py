from django import forms
# Se importan los modelos para poder crear formularios basados en estos modelos, esto permite crear formularios de manera rápida y sencilla utilizando la funcionalidad de ModelForm de Django, lo que facilita la validación y el manejo de datos relacionados con los modelos.
from .models import CreacionUsuario
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'email',
                   'password',
                   'first_name',
                   'last_name'
                   ]
        
class Formulario_Usuario(forms.ModelForm):
    class Meta:
        model = CreacionUsuario
        fields = [ 'departamento',
                   'municipio',
                   'tipo_identificacion',
                   'numero_identificacion',
                   'telefono_1',
                   'telefono_2',
                   'direccion_residencia',
                   'fecha_nacimiento',
                   'fotografia',
                   ]
        
        # widgets = {
        #     'password': forms.PasswordInput(),
        # }