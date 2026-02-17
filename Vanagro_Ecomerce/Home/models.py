from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Mensaje(models.Model):
	fecha_envio= models.DateTimeField('Fecha de envió', auto_now_add=True)
	nombres = models.CharField('Nombres', max_length=50)
	apellido = models.CharField('Apellido', max_length=70)
	telefono = models.PositiveBigIntegerField('Teléfono')
	email = models.EmailField('Correo Electrónico')
	mensaje = models.TextField('Su mensaje')
	estado = models.BooleanField('Estado del mensaje', default=False)
 	
	def __str__(self):
		return f'{self.fecha_envio} -{self.nombres} - {self.apellido} - {self.estado}'