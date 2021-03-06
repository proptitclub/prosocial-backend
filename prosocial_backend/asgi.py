"""
ASGI config for prosocial_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from asgi_cors import asgi_cors

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prosocial_backend.settings")

django_asgi_app = get_asgi_application()

application = asgi_cors(ProtocolTypeRouter({
    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
}), allow_all=True)