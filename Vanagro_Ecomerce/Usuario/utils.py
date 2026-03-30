from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import token_activacion


def generar_link_activacion(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_activacion.make_token(user)   
    dominio = request.get_host()
    protocolo = 'http' 
    
    return f"{protocolo}://{dominio}{reverse('activar_cuenta', kwargs={'uidb64': uid, 'token': token})}"
  

def enviar_correo_activacion(user, link):
    print("LINK ENVIADO:", link)

    html_content = render_to_string('components/activar_cuenta.html', {
        'usuario': user,
        'link_activacion': link,
    })

    email = EmailMultiAlternatives(
        'Activa tu cuenta en Vanagro 🌱',
        f"Activa tu cuenta aquí:\n{link}", 
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()


