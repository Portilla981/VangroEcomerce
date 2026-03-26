import os
from django.core.management.base import BaseCommand
from django.conf import settings
from Usuario.models import CreacionUsuario, CreacionProductor
from Producto.models import Producto

class Command(BaseCommand):
    help = 'Limpiar media'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT

        # Archivos usados en BD
        archivos_usados = set()

        # Productos
        for p in Producto.objects.exclude(imagen_producto=''):
            archivos_usados.add(p.imagen_producto.path)

        # Usuarios
        for u in CreacionUsuario.objects.exclude(fotografia=''):
            archivos_usados.add(u.fotografia.path)

        # Productores
        for p in CreacionProductor.objects.exclude(foto_finca=''):
            archivos_usados.add(p.foto_finca.path)

        eliminados = 0

        # Recorrer carpeta media
        for root, dirs, files in os.walk(media_root):
            for file in files:
                ruta = os.path.join(root, file)

                if ruta not in archivos_usados:
                    print(f"Eliminando: {ruta}")
                    os.remove(ruta)
                    eliminados += 1

        self.stdout.write(self.style.SUCCESS(f'Archivos eliminados: {eliminados}'))