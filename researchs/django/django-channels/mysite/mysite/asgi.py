"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# ProtocolTypeRouter checks the connection type and 
# gives the connection to the established handler
application = ProtocolTypeRouter({
    # Connection protocols: HTTP and WebSockets

    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),
    # Handle WebSockets
    'websocket':AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
