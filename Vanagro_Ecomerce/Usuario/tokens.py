from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenActivacion(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.usuario.verificado)
        
token_activacion = TokenActivacion()