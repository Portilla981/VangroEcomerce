from django.db import models
from django.conf import settings
from Producto.models import Producto
from django.utils import timezone

# Create your models here.

#modelo ItemCarrito
class ItemCarrito(models.Model):
	#cada producto que se agregue al carrito pertenece al usuario
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carrito')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name= 'producto')
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
    	#producto y usuario único (no se repite)
        unique_together = ('usuario', 'producto')

    #calcula el subtotal por producto
    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre_producto}"

