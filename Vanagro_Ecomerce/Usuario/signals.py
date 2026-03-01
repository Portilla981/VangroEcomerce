# Ejecutar algo después de guardar un nuevo usuario.
from django.db.models.signals import post_save
# Importar el modelo User para conectar la señal con el modelo de usuario.
from django.contrib.auth.models import User
# Importar el decorador receiver para conectar la señal con la función que se ejecutará después de guardar un nuevo usuario.
from django.dispatch import receiver
# Importar el modelo CreacionUsuario para crear automáticamente un perfil de usuario asociado al nuevo usuario creado.
from .models import CreacionUsuario 

# Se utiliza el decorador receiver para conectar la señal post_save del modelo User con la función de Creacion de usuario.
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        CreacionUsuario.objects.create(user=instance)
        # Función de creación de perfil de usuario, esta función se ejecutará cada vez que se guarde un nuevo usuario, y si el usuario es creado (created=True), se creará automáticamente un perfil de usuario asociado a ese nuevo usuario utilizando el modelo CreacionUsuario.
