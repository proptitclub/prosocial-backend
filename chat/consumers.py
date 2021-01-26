# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *


class ChatConsumer(AsyncWebsocketConsumer):
    '''
        SYNC DEF
    '''
    def check_room_user(self):
        self.room = Room.objects.get(name=self.room_name)
        if self.room is None:
            return False
        return True

    def save_message(self, info):
        self.room = room.objects.get(name=self.room_name)
        user_room = UserRoom(user=self.user, room=self.room)
        message = Message(user_room = user_room, content = info.get('content'), type=info.get('type'))
        message.save()
        return message

    '''
        ASYNC DEF
    '''
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']
        is_allow = await database_sync_to_async(self.check_room_user)()

        # is_allow = False
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        message = await database_sync_to_async(self.save_message)(text_data_json)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
