from django.db import models

from django.contrib.auth.models import User

from django.core.validators import MinValueValidator
from decimal import Decimal
# Register your models here.

class Producto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='producto')
        
    nombre_producto = models.CharField('Nombre Producto',max_length=200)
    descripcion = models.TextField()
    #decimal con 10 digitos y 2 decimales
    precio = models.DecimalField('Precio Producto',max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    #almacenar la imagen. Se almacena en la carpeta media
    imagen = models.ImageField('Foto Producto',upload_to='productos/', blank=True, null=True)
    #restricción de que solo sean numeros positivos
    stock = models.PositiveIntegerField('Cantidad',default=0)
    #estado del producto
    activo = models.BooleanField('Habilitado',default=True)
    
    def save(self, *args, **kwargs):
        # Si el stock llega a 0 se desactiva automáticamente
        if self.stock == 0:
            self.activo = False
        #else:
            #self.activo = True

        #Despues de ejecutar la regla, se ejecuta el método save como Django lo realiza
        #si esta línea no se coloca, no se actualiza en bd
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f'Producto: {self.nombre} - Cantidad:{self.stock} '