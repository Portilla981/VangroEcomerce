from django.db import models
from django.contrib.auth.models import User

class EstadoMensaje(models.TextChoices):
    PENDIENTE = 'pendiente', 'Pendiente'
    PROCESO = 'en_proceso', 'En proceso'
    RESUELTO = 'resuelto', 'Resuelto'

# Create your models here.
class Mensaje(models.Model):
	fecha_envio= models.DateTimeField('Fecha de envió', auto_now_add=True)
	asunto = models.CharField('Asunto', max_length=150)
	nombres = models.CharField('Nombres', max_length=50)
	apellidos = models.CharField('Apellidos', max_length=70)
	telefono = models.CharField('Teléfono', max_length=15)
	email = models.EmailField('Correo Electrónico')
	mensaje = models.TextField('Su mensaje')
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	tipo = models.CharField(max_length=20, choices=[('publico', 'Público'),('usuario', 'Usuario'),],default='publico')
	estado = models.CharField(max_length=20, choices=EstadoMensaje.choices, default=EstadoMensaje.PENDIENTE)
	respuesta = models.TextField(blank=True, null=True)
	atendido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mensajes_atendidos')
	fecha_respuesta = models.DateTimeField(null=True, blank=True)
 	
	def __str__(self):
		return f'{self.fecha_envio} - {self.nombres} {self.apellidos} - {self.estado}'