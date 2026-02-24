from django.db import models

# Importación del modelo de usuario de Django para extenderlo o relacionarlo con otros modelos
from django.contrib.auth.models import User

# Register your models here.

# se crean los modelos para el departamento y municipio, para luego relacionarlos con el modelo de usuario y así tener una mejor organización de la información de los usuarios en la base de datos.
class Departamento(models.Model):
    nombre_Departamento = models.CharField('Departamento', max_length=100)

    def __str__(self):
        return self.nombre_Departamento

class Municipio(models.Model):
    nombre_Municipio = models.CharField('Municipio', max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_Municipio

# Se crea el modelo de identificación para almacenar los diferentes tipos de identificación que pueden tener los usuarios, como cédula de ciudadanía, cédula de extranjería, pasaporte, entre otros, asi se puede tener a futuros tipos de identificacion.
class Identificacion(models.Model):
    tipo_identificacion = models.CharField('Tipo de Identificación', max_length=50)

    def __str__(self):
        return self.tipo_identificacion
    


class CreacionUsuario(models.Model):
    # Relación uno a uno con el modelo de usuario de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    # Campos adicionales para el perfil del usuario
    # Relación para listas desplegables de tipo de identificación, departamento y municipio
    tipo_identificacion = models.ForeignKey(Identificacion, on_delete=models.SET_NULL, null=True, blank=True)
    # Este campo debe ser único para cada usuario, por lo que se establece unique=True para evitar duplicados en la base de datos, ademas se debe de validar que solo sean números.   
    numero_identificacion = models.CharField('Número de Identificación', max_length=20, blank=True, unique=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True)
    telefono_1 = models.CharField('Teléfono', max_length=20, blank=True)
    telefono_2 = models.CharField('Teléfono Alterno', max_length=20, blank=True)
    direccion_residencia = models.CharField('Dirección', max_length=255, blank=True)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', null=True, blank=True)
    fotografia = models.ImageField('Fotografía', upload_to='usuarios/', default='usuarios/usuario_default.png', blank=True, null=True)



    def __str__(self):  
        return self.user.username
