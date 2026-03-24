from django.db import models
from django.contrib.auth.models import User
from Producto.models import Producto

# Create your models here.
class Pedido(models.Model):
    ESTADOS = [('Pagado', 'Pagado'), ('Pendiente', 'Pendiente'), ('Cancelado', 'Cancelado'),]
    #cada pedido pertenece a un usuario
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    #fecha automática
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    #toma los valor de ESTADOS por defecto es Pagado
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pagado')

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"


class DetallePedido(models.Model):
    #se relaciona con Pedido
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    #se relaciona con Producto
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    despachado = models.BooleanField(default=False)

    def subtotal(self):
        return self.cantidad * self.precio

    def __str__(self):
        return f"{self.producto.nombre_producto} x {self.cantidad}"