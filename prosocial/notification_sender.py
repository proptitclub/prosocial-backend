from abc import ABC

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from datetime import datetime
from .models import *
from django.db.models import QuerySet
# custom TokenObtain view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import requests
import json

APP_ID = '913dba2c-9869-4355-a68e-5be7321465c9'
REST_API_ONESIGNAL_ID = 'ZDg4NTNmNmItYzYxNi00ZjhiLWJmYmQtM2RiOGQ2ZjJhN2Iy'
REST_API_URL = 'https://onesignal.com/api/v1/notifications'


class NotificationSender:
    serializer = NotificationSerializer
    
    @staticmethod
    def serialize_and_send(noti_mem) -> None:
        payload = NotificationSender.create_payload(noti_mem)
        if payload == None:
            print("User device is not exist for this user")
            return
        
        header = {
            "Content-Type": "application/json; charset=utf-8",
        }

        # tạm ngắt tính năng này vì chưa có phần obtain user_id
        # req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))


        return
    
    @staticmethod
    def create_payload(noti_mem) -> dict:
        try:
            user_device = UserDevice.objects.get(assigned_user=noti_mem.assigned_user)
        except:
            return None
        content = NotificationMemberSerializer(noti_mem).data
        return {
            "app_id": APP_ID,
            "include_player_ids": [user_device.device_id],
            "contents": {
                "vi": message,
            },
            "data": content
        }
    
    @staticmethod
    def create_noti(*args, **kwargs):
        pass

class CreatingPostSender(NotificationSender):
    message_template = "{} đã đăng một bài viết trong nhóm {}"

    @staticmethod
    def create_noti(obj: Post) -> None:
        post = obj
        assigned_group = post.assigned_group
        members_take_noti = (assigned_group.members | assigned_group.admins).distinct()
        new_noti = Notification(assigned_user=obj.assigned_user, assigned_post=obj.assigned_post, type=0)
        new_noti.save()
        for member in members_take_noti:
            new_member_noti = NotificationMember(assigned_member=member, assigned_notification=new_noti)
            new_member_noti.save()
            CreatingPostSender.serialize_and_send(new_member_noti, CreatingPostSender.message_template)
        
        return

class ReactionSender(NotificationSender):

    message_template = "{} đã bày tỏ cảm xúc về một bài viết trong nhóm {}"

    @staticmethod
    def create_noti(obj: Reaction) -> None:
        post = obj.assigned_post
        assigned_group = post.assigned_group
        members_take_noti = (assigned_group.members.all() | assigned_group.admins.all()).distinct()
        new_noti = Notification(assigned_user=obj.assigned_user, assigned_post=obj.assigned_post, type=1)
        new_noti.save()
        for member in members_take_noti:
            print(member.id, member.display_name, member.username)
            new_member_noti = NotificationMember(assigned_user=member, assigned_notification=new_noti)
            new_member_noti.save()
            ReactionSender.serialize_and_send(new_member_noti, ReactionSender.message_template)

        return


class CommentSender(NotificationSender):
    
    message_template = "{} đã bình luận về một bài viết trong nhóm {}"

    @staticmethod
    def create_noti(obj: Comment) -> None:
        post = obj.assigned_post
        assigned_group = post.assigned_group
        members_take_noti = (assigned_group.members.all() | assigned_group.admins.all()).distinct()
        new_noti = Notification(assigned_user=obj.assigned_user, assigned_post=obj.assigned_post, type=1)
        new_noti.save()
        for member in members_take_noti:
            print(member.id, member.display_name, member.username)
            new_member_noti = NotificationMember(assigned_user=member, assigned_notification=new_noti)
            new_member_noti.save()
            ReactionSender.serialize_and_send(new_member_noti, CommentSender.message_template)

        return