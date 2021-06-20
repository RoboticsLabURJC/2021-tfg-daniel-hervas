# Django researchs

## Crear espacio de trabajo
		django-admin startproject <nombre>

## Estructura de directorios
	mysite/
		manage.py
		mysite/
			__init__.py
			settings.py
			urls.py
			asgi.py
			wsgi.py
	
- outer mysyte: es el directorio raiz para el proyecto, se puede renombrar
al nombre que se quiera, no importa para Django.

- manage.py: Una utilidad de la línea de comandos que le permite 
interactuar con este proyecto Django de diferentes formas.

- En interior del directorio mysite/ es el propio paquete de Python para
 su proyecto. Su nombre es el nombre del paquete de Python que usted 
 tendrá que utilizar para importar todo dentro de este (por ejemplo, mysite.urls).

- mysite/__init__.py: Un archivo vacío que le indica a Python que este 
directorio debería ser considerado como un paquete Python.

- mysite/settings.py: Ajustes/configuración para este proyecto Django.

- mysite/urls.py: Las declaraciones URL para este proyecto Django; una 
«tabla de contenidos» de su sitio basado en Django.

- mysite/asgi.py: mysite/wsgi.py: Un punto de entrada para que los servidores web compatibles con ASGI puedan servir su proyecto.

- mysite/wsgi.py: Un punto de entrada para que los servidores web compatibles con WSGI puedan servir su proyecto.


## Lanzar servidor de desarrollo
		python manage.py runserver
		
## Crear una aplicación
		python manage.py startapp polls
		
Esto crea un directiorio llamando polls:
	polls/
		__init__.py
		admin.py
		apps.py
		migrations/
			__init__.py
		models.py
		tests.py
		views.py
		
## Models
### Migrate
	python manage.py migrate
Crea en la base de datos de Django las tablas necesarias para las apps instaladas
y settings.py

### Makemigrations
	python manage.py makemigrations
Siempre debemos incluir las aplicaciones en settings.py.
Sirve para indicar a Django que hemos realizado cambios en los modelos de
la aplicación, esto genera las tablas necesarias para los modelos.

### Superuser
		python manage.py createsuperuser
