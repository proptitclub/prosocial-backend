from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url
import chat.consumers as consumers
from chat.jwt_authentication import TokenAuthMiddlewareStack
# from home.consumers import MessageConsumer, EditorConsumer
import json
import django
import os
from django.urls import re_path
# from chat.consumers import app
# import chat.routing
import socketio
from chat.consumers import sio


websocket_urlpatterns = [
    # url('socket/streaming/', MessageConsumer),
    # url('socket/editor/', EditorConsumer)
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prosocial_backend.settings')
django.setup()

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddlewareStack(
    	URLRouter(
            websocket_urlpatterns
    	)
    )
})