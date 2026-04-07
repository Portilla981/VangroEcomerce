from django import forms
# Se importan los modelos para poder crear formularios basados en estos modelos, esto permite crear formularios de manera rápida y sencilla utilizando la funcionalidad de ModelForm de Django, lo que facilita la validación y el manejo de datos relacionados con los modelos.
from .models import CreacionUsuario, Municipio, CreacionProductor
from django.contrib.auth.models import User
# Esto es para validar el campo de identificacion que acepte solo números o letras
import re
from datetime import date
from django.core.exceptions import ValidationError

# Funcion global para formatear textos cuando se necesite que la primera letra sea en mayúscula
def fomato_texto(texto):
    if texto:
        texto = texto.strip().lower()  # Eliminar espacios al inicio y final y convertir a minúsculas
        #texto = texto.capitalize()  # Convertir la primera letra a mayúscula
        palabras = texto.split()  # Reemplazar múltiples espacios por uno solo
        # Capitalizar cada palabra y unirlas con un espacio
        return " ".join(p.capitalize() for p in palabras)


class UserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                   'first_name',
                   'last_name'
                   ]
        
    # Se valida que loq ue se ingrese cambie a mayúscula la primera letra y el resto en minúscula, 
    def clean_first_name(self):
        nombre = self.cleaned_data.get('first_name')
        if nombre:
            return fomato_texto(nombre)
        return nombre
    
    def clean_last_name(self):
        apellido = self.cleaned_data.get('last_name')
        if apellido:
            return fomato_texto(apellido)
        return apellido
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower() # Normalizamos a minúsculas
            # Buscamos si ya existe alguien con ese correo (excluyendo al propio usuario si es edición)
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Ya existe una cuenta asociada a este correo electrónico")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas ingresadas no coinciden")
        

class Form_Actualizar_User(forms.ModelForm):

    class Meta:
        model = User
        fields =[
            'first_name',
            'last_name',
            'email'
        ]

#========================================================        
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
        tipo = self.cleaned_data.get('tipo_identificacion')  

        if not num: 
            return num 
                 
        # Eliminar espacios al inicio y final
        num = num.strip().replace(" ", "").upper()         
        
        # Validar el formato del número de identificación según el tipo seleccionado
        if tipo and tipo.id == 1:
            # Forma natural y camino paso a paso para validar
            # if not num.isdigit():
            #     raise forms.ValidationError("El número de identificación debe contener solo números para este tipo de identificación")
            
             # No puede empezar por 0
            # if num.startswith("0"):
            #     raise forms.ValidationError("La cédula no puede comenzar con cero.")
            
            # Forma simple de ahorrar código para validar que sean números y q no comience por 0
            if not re.match(r'^[1-9][0-9]*$', num):
                raise forms.ValidationError("El número de cédula debe ser numérico y no puede comenzar con cero")

        # Para los otro tipos de identificacion, se permite la combinacion de números y letras
        else:
            if not re.match(r'^[A-Za-z0-9]+$', num):
                raise forms.ValidationError("El número de identificación debe contener únicamente letras y números")
        
        # Colocar el número de identificación en mayúsculas y sin espacios
        if num:
            num = num.strip().upper()
            
        buscare = CreacionUsuario.objects.filter(numero_identificacion= num)

        if self.instance.pk:
            buscare = buscare.exclude(pk=self.instance.pk)

        
        if buscare.exists():
            raise forms.ValidationError("Este número de identificación ya se encuentra registrado en nuestro sistema.")
        
        return num
    
    def clean_telefono_1(self):
        telefono = self.cleaned_data.get('telefono_1')
        if not telefono.isdigit():
            raise forms.ValidationError("El número de teléfono debe contener únicamente dígitos numéricos")
        
        # Validar longitud si es necesario
        if len(telefono) != 10:
            raise forms.ValidationError("El número de teléfono debe tener exactamente 10 dígitos")
        
        return telefono

    def clean_telefono_2(self):
        telefono = self.cleaned_data.get('telefono_2')
        
        # 1. Si el teléfono es None o está vacío, simplemente lo retornamos (no es obligatorio)
        if not telefono:
            return telefono
        
        if not telefono.isdigit():
            raise forms.ValidationError("El número de teléfono alterno debe contener únicamente dígitos numéricos.")
        
        # Validar longitud si es necesario
        if len(telefono) != 10:
            raise forms.ValidationError("El número de teléfono alterno debe tener exactamente 10 dígitos.")
                       
        return telefono
    
    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        hoy = date.today()
        
        # Cálculo exacto de edad
        edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
        
        if edad < 18:
            raise ValidationError("Usted debe ser mayor de 18 años para realizar el registro.")
        
        return fecha

        
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
                #    'latitud',
                #    'longitud',
                   'descripcion',
                #    'activo'
                   ]
        
    def clean_nombre_finca(self):
        nombre = self.cleaned_data.get('nombre_finca')
        if nombre:
            return fomato_texto(nombre)
        return nombre
    
    def clean_vereda(self):
        vereda = self.cleaned_data.get('vereda')
        if vereda:
            return fomato_texto(vereda)
        return vereda
    
    def clean_foto_finca(self):
        foto = self.cleaned_data.get('foto_finca')
        if foto:
            if foto.size > 5 * 1024 * 1024:  # Limitar a 5MB
                raise forms.ValidationError("El archivo seleccionado es demasiado grande. El tamaño máximo permitido es de 5 MB")
        return foto
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'departamento' in self.data:
            dep_id = self.data.get('departamento')
            self.fields['municipio'].queryset = Municipio.objects.filter(departamento_id=dep_id)
        else:
            self.fields['municipio'].queryset = Municipio.objects.none()