from django import forms

from .models import *

class Form_contacto(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ('nombres', 'apellido', 'telefono', 'email', 'mensaje')
        
