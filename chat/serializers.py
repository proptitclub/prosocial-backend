from django.contrib.auth.models import User

from rest_framework import serializers

from .models import *

class RoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    def get_last_message(self, obj):
        request = self.context.get('request')
        user_rooms = UserRoom.objects.filter(room=obj)
        last_message = Message.objects.filter(user_room___in=user_rooms).order_by('-created_time')[0]
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
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        request = self.context.get('request')
        user = obj.user_room.user
        return AssignedUserSummary(user, context={"request": request}).data
    
    
    class Meta:
        model = Message
        fields = [
            "user",
            "content",
            "created_time",
            "type",
        ]
    