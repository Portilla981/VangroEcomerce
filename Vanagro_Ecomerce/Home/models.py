from django.db import models

# Create your models here.
class Mensaje(models.Model):
	fecha_envio= models.DateTimeField('Fecha de envio', auto_now_add=True)
	nombres = models.CharField('Nombres', max_length=50)
	apellido = models.CharField('Apellido', max_length=70)
	telefono = models.PositiveBigIntegerField('Telefono', max_length=20)
	email = models.EmailField('Correo Electronico')
	mensaje = models.TextField('Su mensaje')
        
    # def __str__(self):
    #     return f'{self.nombres} - {self.apellidos}'