from django.apps import AppConfig

class UsuarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Usuario'

    # Se crea el método ready para importar las señales de creación de usuario, esto permite ejecutar código personalizado cada vez que se crea un nuevo usuario, como crear automáticamente un perfil de usuario asociado al nuevo usuario.
    # Se extiende al archivo signals.py para manejar la creación automática del perfil de usuario cada vez que se crea un nuevo usuario en el sistema, esto se logra utilizando señales de Django para escuchar el evento de creación de un nuevo
    def ready(self):
        import Usuario.signals
