from django import forms

from .models import *

class Form_contacto(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ('Nombres', 'Apellidos', 'Telefono', 'Mesaje')
