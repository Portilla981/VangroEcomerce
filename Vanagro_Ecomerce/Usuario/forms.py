from django import forms
# Se importan los modelos para poder crear formularios basados en estos modelos, esto permite crear formularios de manera rápida y sencilla utilizando la funcionalidad de ModelForm de Django, lo que facilita la validación y el manejo de datos relacionados con los modelos.
from .models import CreacionUsuario, Municipio, CreacionProductor
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                   'first_name',
                   'last_name'
                   ]
    
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        
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
        
          
    def clean_numero_identificacion(self):
        num = self.cleaned_data['numero_identificacion']
        if CreacionUsuario.objects.filter(numero_identificacion = num).exists():
            raise forms.ValidationError("Este número de identificación ya existe")
        return num
   
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'departamento' in self.data:
            dep_id = self.data.get('departamento')
            self.fields['municipio'].queryset = Municipio.objects.filter(departamento_id=dep_id)
        else:
            self.fields['municipio'].queryset = Municipio.objects.none()


class Formulario_Productor(forms.ModelForm):
    class Meta:
        model = CreacionProductor
        fields = [ 'nombre_finca',
                   'departamento',
                   'municipio', 
                   'vereda',
                   'direccion',
                   'foto_finca',
                   'latitud',
                   'longitud',
                   'descripcion',
                   'activo'
                   ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'departamento' in self.data:
            dep_id = self.data.get('departamento')
            self.fields['municipio'].queryset = Municipio.objects.filter(departamento_id=dep_id)
        else:
            self.fields['municipio'].queryset = Municipio.objects.none()