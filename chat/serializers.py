from django.contrib.auth.models import User

from rest_framework import serializers

from .models import *

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "name",
        ]