"""
WSGI config for prosocial_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prosocial_backend.settings")

application = get_wsgi_application()

import socketio
from chat.consumers import sio
# sio = socketio.Server(
#     async_mode='gevent_uwsgi',
#     cors_allowed_origins=["http://localhost:3000"],
#     logger=True,
#     engineio_logger=True,
# )

application = socketio.WSGIApp(sio, application)