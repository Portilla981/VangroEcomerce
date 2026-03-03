from django.db import models

from django.contrib.auth.models import User
# Importación de elementos para validar el precio del producto
from django.core.validators import MinValueValidator
from decimal import Decimal

# Register your models here.

class Producto(models.Model):
    UNIDAD_MEDIDA = [('Kg', 'Kilogramos'), ('Lt', 'Litros'), ('Lb', 'Libras'),('N/A', 'Sin medida'),('Und', 'Unidad'),]
    CATEGORIA = [('Frutas', 'Frutas'), ('Verduras', 'Verduras'), ('Granos', 'Granos'), ('Lácteos', 'Lácteos'), ('Carnes', 'Carnes'), ('Otros', 'Otros')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='producto')
        
    nombre_producto = models.CharField('Nombre Producto',max_length=200)

    unidad_medida = models.CharField('Unidad de medida', max_length=50, choices=UNIDAD_MEDIDA, default='N/A')

    categoria = models.CharField('Categoría', max_length=20, choices=CATEGORIA, default='Otros') 

    caducidad = models.BooleanField('¿El producto tiene fecha de caducidad?', default=False)
    fecha_elaboracion = models.DateField('Fecha de elaboración', blank=True, null=True)
    fecha_vencimiento = models.DateField('Fecha de vencimiento', blank=True, null=True)
    
    descripcion = models.TextField('descripción del producto', blank=True, null=True)
    #decimal con 10 dígitos y 2 decimales
    precio = models.DecimalField('Precio Producto',max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    #almacenar la imagen. Se almacena en la carpeta media
    imagen = models.ImageField('Foto Producto',upload_to='productos/', blank=True, null=True)
    #restricción de que solo sean números positivos
    stock = models.PositiveIntegerField('Cantidad',default=0)
    #estado del producto
    activo = models.BooleanField('Habilitado',default=True)
    
    def save(self, *args, **kwargs):
        # Si el stock llega a 0 se desactiva automáticamente
        if self.stock == 0:
            self.activo = False
        #else:
            #self.activo = True

        #Después de ejecutar la regla, se ejecuta el método save como Django lo realiza
        #si esta línea no se coloca, no se actualiza en bd
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f'Producto: {self.nombre} - Cantidad:{self.stock} '