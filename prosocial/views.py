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
from .notification_sender import *
from rest_framework.decorators import action

APP_ID = '913dba2c-9869-4355-a68e-5be7321465c9'
REST_API_ONESIGNAL_ID = 'ZDg4NTNmNmItYzYxNi00ZjhiLWJmYmQtM2RiOGQ2ZjJhN2Iy'

def send_to_onesignal_worker(app_id, include_player_ids, contents):
    header = {"Content-Type": "application/json; charset=utf-8"}

    payload = {"app_id": app_id,
            "include_player_ids": include_player_ids,
            "contents": {"vi": contents}}
    
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
    
    print(req.status_code, req.reason)


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = CustomMember.objects.all()
    serializer_class = CustomMemberSerializer


# class AccountViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = Member.objects.all()
#     serializer_class = MemberSerializer


class GroupViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = GroupPro.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostSummary
        if self.action == 'retrieve':
            return PostSerializer
        return PostSerializer

    def get_queryset(self):
        request = self.request
        user = request.user
        posts = Post.objects.all()
        filtered_posts = posts
        response_info = []
        params = dict(request.query_params)
        method = params.get('method')
        # print(method)
        if method is not None:
            if method[0] == 'byUser':
                user = CustomMember.objects.get(id=params.get('id')[0])
                filtered_posts = Post.objects.filter(assigned_user=user)
            if method[0] == 'byGroup':
                group = GroupPro.objects.get(id=params.get('id')[0])
                filtered_posts = Post.objects.filter(assigned_group=group)

        return filtered_posts

    def create(self, request, *args, **kwargs):
        group_id = request.data.get("group_id")
        content = request.data.get("content")
        post_type = request.data.get("type")
        time_create = datetime.now()
        new_post = Post(
            assigned_user=request.user,
            assigned_group=GroupPro.objects.get(id=group_id),
            content=content,
            time=time_create,
            type=post_type,
        )
        new_post.save()
        print(request.FILES)
        print(request.FILES.getlist("files"))
        count_ = 0
        for count, x in enumerate(request.FILES.getlist("files")):

            def process(f):
                image = Image(img_url=f)
                image.save()
                new_post.photos.add(image)
            count_ = count
            process(x)
        # print(count)

        print("this post has {} files".format(count_))
        new_post.save()

        new_notification = Notification(
            assigned_post=new_post,
            assigned_user=request.user,
            type=0
        )
        new_notification.save()
        user_list = new_post.assigned_group.members
        
        relation_device_id_list = []
        for user in user_list.all():
            print('{} == {}'.format(user.id, request.user.id))
            if user.id == request.user.id:
                continue
            new_notification_member = NotificationMember(assigned_user=user, assigned_notification=new_notification)
            new_notification_member.save()
            user_device_list = UserDevice.objects.filter(assigned_user=user)
            for user_device in user_device_list:
                relation_device_id_list.append(user_device.device_id)
        
        send_to_onesignal_worker(APP_ID, relation_device_id_list, 'Đây là notification từ post {}'.format(new_post.id))
        
        return PostSerializer(new_post, context={'request': request}).data

    def update(self, request, *args, **kwargs):
        user = request.user
        post = Post.objects.get(id=kwargs["pk"])
        content = request.data.get("content")
        time_update = datetime.now()
        post.__dict__.update({"content": content})
        post.__dict__.update({"time": time_update})
        post.save()

        return Response({"status": "DONE"})

    def delete(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs["pk"])
        reactions_list = Reaction.objects.filter(assigned_post=post)
        for reaction in reactions_list:
            reaction.delete()
        comments_list = Comment.objects.filter(assigned_post=post)
        for comment in comments_list:
            comment.delete()
        post.delete()


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        super().get_queryset()
        # print("it reached here" + "!"*10)
        # print(self.kwargs)
        post_id = self.request.query_params.get('post_id', None)
        if post_id != None:
            post = Post.objects.get(id=post_id)
            return Comment.objects.filter(assigned_post=post)
        else:
            return Comment.objects.all()

    def update(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=kwargs["pk"])
        content = request.data.get("content")

        comment.__dict__.update({"content": content})
        comment.save()
        return Response({"status": "Done"})

    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data.get("post_id")
        post = Post.objects.get(id=post_id)
        content = request.data.get("content")
        new_comment = Comment(assigned_user=user, assigned_post=post, content=content)
        new_comment.save()
        return Response({"status": "Done"})

    def delete(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=kwargs["pk"])
        comment.delete()
        return Response({"status": "Done"})


class ReactionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer


    def update(self, request, *args, **kwargs):
        reaction = Reaction.objects.get(id=kwargs["pk"])
        content = request.data.get("type")

        reaction.__dict__.update({"type": content})
        reaction.save()
        return Response({"status": "Done"})

    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data.get("post_id")
        post = Post.objects.get(id=post_id)
        content = request.data.get("type")
        new_reaction = Reaction(assigned_user=user, assigned_post=post, type=content)
        new_reaction.save()
        ReactionSender.create_noti(request, new_reaction)
        return Response({"reaction_id": new_reaction.id})



class PollViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class TickViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Tick.objects.all()
    serializer_class = TickSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        poll_id = request.data.get('poll_id')
        new_tick = Tick(assigned_user=user, assigned_poll=Poll.objects.get(id=poll_id))
        new_tick.save()
        return Response({'tick_id': new_tick.id})

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # print(user)
        token = super().get_token(user)
        # print(type(token))
        token["id"] = user.id
        # print(token)
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(assigned_user=user)


class NotificationMemberViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationMemberSerializer

    def get_queryset(self):
        user = self.request.user
        return NotificationMember.objects.filter(assigned_user=user)

class NewsFeedViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSummary

    def get_queryset(self):
        user = self.request.user
        attended_group_as_member = GroupPro.objects.filter(members__in=[user])
        attended_group_as_admin = GroupPro.objects.filter(admins__in=[user])
        attended_group = (attended_group_as_admin | attended_group_as_member).distinct()

        list_post = Post.objects.none()
        for group in attended_group:
            list_post = list_post | Post.objects.filter(assigned_group=group)
        list_post = list_post.distinct()
        return list_post

class PointViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PointSerializer

    def get_queryset(self):
        return Point.objects.all()

class TargetViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TargetSerializer

    def get_queryset(self):
        request = self.request
        user = self.request.user
        params = dict(request.query_params)
        method = params.get('method')
        query_set = Target.objects.all()
        # print(method)
        if method is not None:
            if method[0] == 'currentMonth':
                cur_month = datetime.today().replace(day=1)
                print(user)
                query_set = Target.objects.filter(created_time__gt=cur_month, assigned_user=user)
        return query_set

class BonusPointViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = BonusPointSerializer

    def get_queryset(self):
        request = self.request
        user = self.request.user
        params = dict(request.query_params)
        method = params.get('method')
        query_set = BonusPoint.objects.all()
        if method is not None:
            if method[0] == 'currentMonth':
                cur_month = datetime.today().replace(day=1)
                query_set = Target.objects.filter(created_time__gt=cur_month, assigned_user=user)
        return query_set

    @action(detail=False, methods=['get'])
    def current_month(self, request, pk=None):
        request = request
        user = request.user
        params = dict(request.query_params)
        method = params.get('method')
        query_set = BonusPoint.objects.all()
        if method is not None:
            if method[0] == 'currentMonth':
                cur_month = datetime.today().replace(day=1)
                query_set = Target.objects.filter(created_time__gt=cur_month, assigned_user=user)
        return Response(BonusPointSerializer(query_set, many=True).data)



