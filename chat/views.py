from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from prosocial.serializers import *
from django.http import JsonResponse
from .models import *
import json
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, DjangoMultiPartParser, JSONParser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.decorators import action, api_view, permission_classes, parser_classes, renderer_classes
from djangorestframework_camel_case.parser import CamelCaseFormParser, CamelCaseMultiPartParser, CamelCaseJSONParser

from djangorestframework_camel_case.render import CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer

from rest_framework.renderers import JSONRenderer
# from djangorestframework_camel_case import CamelCaseJSONEncoder


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

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@parser_classes([MultiPartParser,])
@renderer_classes([CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer,])
def get_room_message(request, room_name):
    room = Room.objects.get(id=room_name)
    messages = Message.objects.filter(user_room__room=room).order_by('created_time')
    message_responses = []
    for message in messages:
        message_response = {}
        message_response.update({"type": message.type})
        message_response.update({"content": message.content})
        user_info = AssignedUserSummary(message.user_room.user, context={'request': request}).data
        message_response.update({"user_room": user_info})
        message_responses.append(message_response)
    return Response(message_responses)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@parser_classes([MultiPartParser,])
def send_image(request, room_name):
    room = Room.objects.get(id=room_name)
    user = request.user
    user_room = UserRoom.objects.get(user=user, room=room)
    count_ = 0
    message = Message(user_room=user_room)
    for count, x in enumerate(request.FILES.getlist("files")):
        def process(f):
            image = Image(img_url=f)
            image.save()
            message.content = image.img_url
            message.type = MessageType.IMAGE.value
        count_ = count
        process(x)
    
    message.save()

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@parser_classes([MultiPartParser,])
def send_audio(request, room_name):
    room = Room.objects.get(id=room_name)
    user = request.user
    user_room = UserRoom.objects.get(user=user, room=room)
    count_ = 0
    message = Message(user_room=user_room)
    for count, x in enumerate(request.FILES.getlist("files")):
        def process(f):
            audio = Audio(img_url=f)
            audio.save()
            message.content = audio.img_url
            message.type = MessageType.AUDIO.value
        count_ = count
        process(x)
    
    message.save()

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@parser_classes([MultiPartParser,])
def send_video(request, room_name):
    room = Room.objects.get(id=room_name)
    user = request.user
    user_room = UserRoom.objects.get(user=user, room=room)
    count_ = 0
    message = Message(user_room=user_room)
    for count, x in enumerate(request.FILES.getlist("files")):
        def process(f):
            video = Video(img_url=f)
            video.save()
            message.content = video.img_url
            message.type = MessageType.VIDEO.value
        count_ = count
        process(x)
    
    message.save()
