from django import forms
from .models import Producto
from django.contrib.auth.models import User

import re

# Funcion global para formatear textos cuando se necesite que la primera letra sea en mayúscula
def fomato_texto(texto):
    if texto:
        texto = texto.strip().lower()  # Eliminar espacios al inicio y final y convertir a minúsculas
        #texto = texto.capitalize()  # Convertir la primera letra a mayúscula
        palabras = texto.split()  # Reemplazar múltiples espacios por uno solo
        # Capitalizar cada palabra y unirlas con un espacio
        return " ".join(p.capitalize() for p in palabras)

class Form_producto(forms.ModelForm):
    
    class Meta:
        model = Producto
        exclude = ['productor', 'estado_producto'] # Excluir el campo 'user' para que no se muestre en el formulario
        
       
    def clean_nombre_producto(self):
        nombre = self.cleaned_data.get('nombre_producto')
        if nombre:
            return fomato_texto(nombre)
        return nombre
    
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if isinstance(precio, str):
            precio = precio.replace(',', '.')
        return precio
    
    def clean(self):
        # 1. Obtenemos todos los datos limpios del formulario
        cleaned_data = super().clean()
        fecha_e = cleaned_data.get("fecha_elaboracion")
        fecha_v = cleaned_data.get("fecha_vencimiento")

        # 2. Comparamos
        if fecha_e and fecha_v:
            if fecha_v <= fecha_e:
                # 3. Lanzamos el error asociado al campo específico
                self.add_error('fecha_vencimiento', "La fecha de caducidad no puede ser anterior a la de elaboracion.")
        
        return cleaned_data
        
    