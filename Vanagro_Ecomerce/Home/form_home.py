from django import forms
from .models import Mensaje

class Form_contacto(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ('asunto', 'nombres', 'apellidos', 'email', 'mensaje')
        
    # def clean_telefono(self):
    #     telefono = self.cleaned_data.get('telefono')

    #     if not telefono:
    #         raise forms.ValidationError("El teléfono es obligatorio")
        
    #     if not telefono.isdigit():
    #         raise forms.ValidationError("El número de teléfono debe contener solo números")
        
    #     # Validar longitud si es necesario
    #     if len(telefono) != 10:
    #         raise forms.ValidationError("El teléfono debe tener 10 dígitos.")
        
    #     return telefono
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields['nombres'].widget.attrs['readonly'] = True
            self.fields['apellidos'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['telefono'].widget.attrs['readonly'] = True