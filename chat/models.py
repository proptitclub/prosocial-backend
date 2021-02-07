from django.db import models
from prosocial.models import *
from .enums import *

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return ""


class UserRoom(models.Model):
    user = models.ForeignKey(CustomMember, on_delete=models.CASCADE, default=None, null=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None, null=False)

    def __str__(self):
        return ""

class Message(models.Model):
    user_room = models.ForeignKey(UserRoom, on_delete=models.CASCADE, default=None, null=False)
    content = models.CharField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)
    type = models.SmallIntegerField(
        null=False,
        blank=False,
        default=MessageType.TEXT.value,
        choices=[
            (MessageType.IMAGE.value, MessageType.IMAGE.name),
            (MessageType.VIDEO.value, MessageType.VIDEO.name),
            (MessageType.AUDIO.value, MessageType.AUDIO.name),
            (MessageType.TEXT.value, MessageType.TEXT.name),
        ],
    )

    def __str__(self):
        return ""