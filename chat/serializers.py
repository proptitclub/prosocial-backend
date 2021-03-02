from django.contrib.auth.models import User

from rest_framework import serializers

from .models import *
from prosocial.serializers import *

class RoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    def get_last_message(self, obj):
        request = self.context.get('request')
        user_rooms = UserRoom.objects.filter(room=obj)
        last_message = Message.objects.filter(user_room__in=user_rooms).order_by('-created_time')[0]
        return MessageSerializer(last_message, context={"request": request}).data
    
    class Meta:
        model = Room
        fields = [
            "url",
            "id",
            "name",
            "last_message"
        ]

class MessageSerializer(serializers.ModelSerializer):
    user_room = serializers.SerializerMethodField()

    def get_user_room(self, obj):
        request = self.context.get('request')
        user = obj.user_room.user
        return AssignedUserSummary(user, context={"request": request}).data
    
    
    class Meta:
        model = Message
        fields = [
            "user_room",
            "content",
            "created_time",
            "type",
        ]
    