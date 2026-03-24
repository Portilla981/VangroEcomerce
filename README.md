# Proyecto Vanagro/Django

Proyecto productivo del SENA.

## Instalación

-> Clonación del repositorio
Ubíquese en el lugar donde va clonar la carpeta del proyecto, debes de tener a la mano la dirección del repositorio dado para trabajar en equipo con lo cual en la linea de código del cmd o bash colocaras 
git clone --branch main --single-branch NOMBRE DEL REPOSITORIO COPIADO Ejm: https://github.com/flia81/VangroEcomerce.git

-> Creación del entrono virtual
Luego abra el proyecto en visual code o el IDE de su preferencia, estando en la raíz del proyecto debe aparecer el archivo README.MD, por oo cual deberá crear un entorno virtual por los comandos de consola
python -m venv Nombre del entrono virtual


-> Activación del entorno virtual
Accede al entorno virtual con: 
cd nombre del entorno virtual\Scripts\activate

-> Copiar los requerimientos que se usaran con el proyecto 
pip install -r dirección donde este el archivo Requirements.txt ejm: "D:\Proyecto_2026\Requerimientos.txt", las comillas son obligatorias si no las usa va tener errores.

-> Preparar la base de datos

cada vez que se realice una clonación es recomendable crear un superusuario por cada miembro del equipo asi cada quien tendrá su propia base de datos, el por q se realiza esto es por seguridad de las contraseñas y demás campos que tiene django.

para las demás tablas y datos seguir lo siguiente
Ingresa al proyecto con cd nombre del proyecto, luego realiza migraciones para actualizar tablas.

manage.py makemigrations
manage.py migrate

Para cargar las bases de datos del proyecto con datos se debe verificar si en el proyecto dentro de cada app (que en sus modelos alojen datos) exista una carpeta llamada fixtures, si no existe hay que crearla con ese nombre, luego ejecutar el comando:

python manage.py loaddata "nombre del archivo".json 
o si esta dentro de app 
python manage.py loaddata "Nombre del archivo"

cuando dentro de una app se creen modelos y se almacene datos para que el proyecto sea igual o que el equipo tenga la misma base de datos se realiza ejecutando el siguiente código:

python manage.py dumpdata usuarios.Departamento usuarios.Municipio --indent 2 > usuarios/fixtures/ubicaciones.json

nota: --indent 2, significa el formato para json sea mas explicito para manejar, si hay actualizaciones de estas tablas realizar el comando para refrescar el script y actualizar los datos

después de dumpdata  se coloca el nombre de la app en minúsculas donde esta el modelo que se quiere copiar sus datos para el equipo, luego el nombre del modelo o de la tabla, si son varias tablas se separa con un espacio, luego el --indent 2 que ya se explico anteriormente, luego después del signo > se coloca la ubicacion donde se va a crear el archivo tipo fixture es decir su ubicacion ejm de ruta usuarios/fixtures/ y luego el nombre que desee con extension .json, esto creara los datos para ser migrados y poder luego extraerlos para acomodar las tablas de la app.



python manage.py runserver

para la accion antes de runserver hay q enviar las variables de entorno tanto GMail como password 'j9dhqvmuwizpifubebm' que son 16 caracteres, debe verse settings para mayor información

Prueba de envio de correo desde shell
from django.core.mail import send_mail

send_mail(
    "Prueba Django",
    "Este es un correo de prueba",
    "tucorreo@gmail.com",
    ["destinatario@gmail.com"],
    fail_silently=False,
)
# Forma de exportar datos con tildes o ñ
python -Xutf8 manage.py dumpdata nombreApp --indent 4 > nombreApp/fixtures/nombre_archivo.json

para cargar los datos utilizar 

python -Xutf8 manage.py loaddata nombre_archivo.json