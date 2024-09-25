"""
ASGI config for GymAdministrationSys project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels import ProtocolTypeRouter, URLRouter
import main.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GymAdministrationSys.settings')

# application = get_asgi_application()
application =  ProtocolTypeRouter({
    'websocket': URLRouter(main.routing.ws_patterns),
})
