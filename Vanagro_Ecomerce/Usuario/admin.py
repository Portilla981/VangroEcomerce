from django.contrib import admin
from .models import *

# Se registran los modelos en el panel de administración de Django para poder gestionarlos desde el admin, esto permite crear, editar y eliminar instancias de estos modelos a través de la interfaz administrativa de Django.

# Register your models here.
admin.site.register(Departamento)
admin.site.register(Municipio)  
admin.site.register(Identificacion)
admin.site.register(CreacionUsuario)
admin.site.register(CreacionProductor)

