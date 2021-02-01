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
from firebase_admin import messaging
import itertools

serverToken = 'AAAAv0K4lCM:APA91bEw20L-m4dDUyV0WmjCh5OQNdhkjXJ_UHrtihYYyWMBRfDDkxkOrANbSt60D5Oahg7tZFpSAczaVONimoDePT4IrVWyLjchMRidVlkbTWTiPYk9q4rbKgvDTOhZmBu8xinJpnyB'

def sendTestNotification(user, text):
    devices = UserDevice.objects.filter(assigned_user=user)
    for device in device:
        deviceToken = 'd9OP08P9RVO8eJKtmp-r-a:APA91bEZ7UAO5aCiHvdDDT1Jk-7PbO5rWfEDHeg2YWH2bjzaCW1gPWXvyydLygbCSztwiQWMTex9HRt8rWdq3b9jEAgtcjEaVE2rI_n_w5FqHsUa0jrjRXB6FnYZ2mTEFOm0Sm-AieOE'

        headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=' + serverToken,
            }

        body = {
                'notification': {'title': 'text',
                                'body': 'New Message'
                },
                'to':
                    deviceToken,
                'priority': 'high',
                #   'data': dataPayLoad,
                }
        response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
        print(response.status_code)

        print(response.text)




class NotificationSender:
    serializer = NotificationSerializer
    
    @staticmethod
    def serialize_and_send(request, noti_mem, message, post_id) -> None:
        user_devices = UserDevice.objects.filter(assigned_user=noti_mem.assigned_user)
        for user_device in user_devices:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=' + serverToken
            }
            body = {
                'notification': {
                    'title': "ProPTIT Social",
                    "body": message,
                },
                'to': user_device.device_id,
                'priority': 'high',
                'data': {
                    "postID": post_id,
                }
            }

            response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
            print(response.status_code)
            print(response.text)
    
    @staticmethod
    def create_payload(request, noti_mem, message) -> dict:
        try:
            user_device = UserDevice.objects.filter(assigned_user=noti_mem.assigned_user)
        except:
            return None
        content = NotificationMemberSerializer(noti_mem, context={'request': request}).data
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
    def create_noti(request, obj: Post) -> None:
        post = obj
        assigned_group = post.assigned_group
        members_take_noti = (assigned_group.members.all() | assigned_group.admins.all()).distinct()
        new_noti = Notification(assigned_user=request.user, assigned_post=obj, type=0)
        new_noti.save()
        for member in members_take_noti:
            new_member_noti = NotificationMember(assigned_user=member, assigned_notification=new_noti)
            message = CreatingPostSender.message_template.format(request.user.display_name, obj.assigned_group.name)
            new_member_noti.save()
            CreatingPostSender.serialize_and_send(request, new_member_noti, message, post.id)
        
        return

class ReactionSender(NotificationSender):

    message_template = "{} đã bày tỏ cảm xúc về một bài viết trong nhóm {}"

    @staticmethod
    def create_noti(request, obj: Reaction) -> None:
        post = obj.assigned_post
        assigned_group = post.assigned_group
        # members_take_noti = (assigned_group.members.all() | assigned_group.admins.all()).distinct()
        member = post.assigned_user
        new_noti = Notification(assigned_user=request.user, assigned_post=obj.assigned_post, type=1)
        new_noti.save()
        # save and send noti
        new_member_noti = NotificationMember(assigned_user=member, assigned_notification=new_noti)
        message = ReactionSender.message_template.format(request.user.display_name, obj.assigned_post.assigned_group.name)
        new_member_noti.save()
        ReactionSender.serialize_and_send(request, new_member_noti, message, post.id)

        return

# class ReactionOnlyCreatorSender(NotificationSender):
#     message_template = "{} đã bày tỏ cảm xúc về một bài viết của bạn"
#     @staticmethod
#     def create_noti(request, obj: Reaction) -> None:
#         post = obj.assigned_post
#         assigned_group = post.assigned_group
#         members_take_noti = (

class CommentSender(NotificationSender):
    
    message_template = "{} đã bình luận về một bài viết trong nhóm {}"

    @staticmethod
    def create_noti(request, obj: Comment) -> None:
        post = obj.assigned_post
        # get user that be sent comment
        list_comments = (Comment.objects.filter(assigned_post=post))
        members_take_noti = CustomMember.objects.filter(id=post.assigned_user.id)
        for comment in list_comments:
            members_take_noti = itertools.chain(members_take_noti, CustomMember.objects.filter(id=comment.assigned_user.id)).distinct()

        new_noti = Notification(assigned_user=request.user, assigned_post=obj.assigned_post, type=1)
        new_noti.save()
        for member in members_take_noti:
            new_member_noti = NotificationMember(assigned_user=member, assigned_notification=new_noti)
            message = CommentSender.message_template.format(request.user.display_name, obj.assigned_post.assigned_group.name)
            new_member_noti.save()
            ReactionSender.serialize_and_send(request, new_member_noti, message, post.id)

        return