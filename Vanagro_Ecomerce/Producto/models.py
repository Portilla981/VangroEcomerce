from django.db import models
from django.contrib.auth.models import User
from Usuario.models import CreacionProductor
# Importación de elementos para validar el precio del producto
from django.core.validators import MinValueValidator
from decimal import Decimal
# Util para agregar fecha de creacion
from django.utils import timezone
from django.core.exceptions import ValidationError

# Register your models here.

class Producto(models.Model):
    UNIDAD_MEDIDA = [('Kg', 'Kilogramos'), ('Lt', 'Litros'), ('Lb', 'Libras'),('N/A', 'Sin medida'),('Und', 'Unidad'),]
    CATEGORIA = [('Frutas', 'Frutas'), ('Verduras', 'Verduras'), ('Granos', 'Granos'), ('Lácteos', 'Lácteos'), ('Otros', 'Otros')]
    ESTADOS = [('borrador', 'Borrador'), ('publicado', 'Publicado')]
    
    productor = models.ForeignKey(CreacionProductor, on_delete=models.CASCADE, related_name='productor')        
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
    imagen_producto = models.ImageField('Foto Producto',upload_to='productos/', blank=True, null=True)
    #restricción de que solo sean números positivos
    stock = models.PositiveIntegerField('Cantidad', default=0)
    # Estado para realizar vista previa 
    estado_producto = models.CharField('Estado del producto', max_length=20, choices=ESTADOS, default='borrador')   
    #estado del producto
    activo = models.BooleanField('Habilitado', default=True)
    # Fecha de creación del producto, se asigna automáticamente al crear el producto
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)

    def clean(self):
        # Primero ejecutamos la limpieza base
        super().clean()

        # Validamos que ambas fechas existan antes de comparar
        if self.fecha_elaboracion and self.fecha_vencimiento:
            if self.fecha_vencimiento <= self.fecha_elaboracion:
                raise ValidationError({
                    'fecha_vencimiento': "La fecha de caducidad debe ser posterior a la fecha de elaboración."
                })

    # def save(self, *args, **kwargs):
    #     # Forzamos la ejecución de clean() antes de guardar en la BD
    #     self.full_clean()
    #     super().save(*args, **kwargs)
   
    def save(self, *args, **kwargs):
        # Si el stock llega a 0 se desactiva automáticamente
        if self.stock == 0:
            self.activo = False
        #else:
            #self.activo = True
        
        # Forzamos la ejecución de clean() antes de guardar en la BD
        self.full_clean()

        #Después de ejecutar la regla, se ejecuta el método save como Django lo realiza
        #si esta línea no se coloca, no se actualiza en bd
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f'Producto: {self.nombre_producto} - Cantidad:{self.stock} '