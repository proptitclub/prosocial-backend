from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from prosocial.serializers import *
from django.http import JsonResponse
from .models import *
import json

def index(request):
    return render(request, 'chat/testchat.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

def get_room_message(request, room_name):
    room = Room.objects.get(id=room_name)
    messages = Message.objects.filter(user_room__room=room)
    message_responses = []
    for message in messages:
        message_response = {}
        message_response.update({"type": message.type})
        message_response.update({"content": message.content})
        user_info = AssignedUserSummary(message.user_room.user, context={'request': request}).data
        message_response.update({"user_room": user_info})
        message_responses.append(message_response)
    return JsonResponse(message_responses, safe=False)