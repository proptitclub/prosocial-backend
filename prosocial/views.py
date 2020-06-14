from abc import ABC

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (
    GroupSerializer,
    PostSerializer,
    CommentSerializer,
    ReactionSerializer,
    PollSerializer,
    TickSerializer,
    CustomMemberSerializer,
)
from datetime import datetime
from .models import GroupPro, Post, Comment, Reaction, Poll, Tick, CustomMember, Image, Notification, NotificationMember, UserDevice

# custom TokenObtain view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import requests
import json

APP_ID = '913dba2c-9869-4355-a68e-5be7321465c9'
REST_API_ONESIGNAL_ID = 'ZDg4NTNmNmItYzYxNi00ZjhiLWJmYmQtM2RiOGQ2ZjJhN2Iy'

def send_to_onesignal_worker(app_id, include_player_ids, contents):
    header = {"Content-Type": "application/json; charset=utf-8"}

    payload = {"app_id": app_id,
            "include_player_ids": include_player_ids,
            "contents": {"en": contents}}
    print(payload)
    
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

    def get_poll_info(self, request, post):
        response = list()
        polls = Poll.objects.filter(assigned_post=post)
        for poll in polls:
            poll_info = dict()
            poll_info['content'] = poll.question
            poll_info['ticks'] = list()
            ticks = Tick.objects.filter(assigned_poll=poll)
            for tick in ticks:
                tick_info = list()
                users = tick.users.all()
                for user in users:
                    user_info = dict()
                    user_info['avatar'] = request.build_absolute_uri(user.avatar.url)
                    user_info['display_name'] = user.display_name
                    user_info['id'] = user.id
                    tick_info.append(user_info)

                poll_info['ticks'].append(tick_info)
            
            response.append(poll_info)

        return response

    def list(self, request, *args, **kwargs):
        user = request.user
        posts = Post.objects.all()
        filtered_posts = posts
        response_info = []
        params = dict(request.query_params)
        method = params.get('method')
        print(method)
        # print(method)
        if method is not None:
            if method[0] == 'byUser':
                user = CustomMember.objects.get(id=params.get('id')[0])
                filtered_posts = Post.objects.filter(assigned_user=user)
            if method[0] == 'byGroup':
                group = GroupPro.objects.get(id=params.get('id')[0])
                filtered_posts = Post.objects.filter(assigned_group=group)

        for post in filtered_posts:
            # print(post.assigned_user.avatar)
            reactions = Reaction.objects.filter(assigned_post = post)
            comments = Comment.objects.filter(assigned_post = post)
            reactions_info = []
            comments_info = []
            info = {
                "id": post.id,
                "content": post.content,
                "assigned_user_id": post.assigned_user.id,
                "assigned_user_avatar": request.build_absolute_uri(post.assigned_user.avatar.url),
                "assigned_user_display_name": post.assigned_user.display_name,
                "assigned_group_id": post.assigned_group.id,
                "assigned_group_name": post.assigned_group.name,
                "reaction_number": len(Reaction.objects.filter(assigned_post=post)),
                "comment_number": len(Comment.objects.filter(assigned_post=post)),
                "time": post.time,
                "type": post.type,
                "photos": list(map(lambda x: request.build_absolute_uri(x.img_url.url), post.photos.all())),
                "reaction_id": Reaction.objects.get(assigned_post=post, assigned_user=user).id if len(Reaction.objects.filter(assigned_post=post, assigned_user=user)) > 0 else -1,
            }
            # response_info.append(info)
            for reaction in reactions:
                reaction_info = {
                    "choice": reaction.type,
                    "assigned_user": reaction.assigned_user.id,
                    "assigned_user_display_name": reaction.assigned_user.display_name,
                }
                reactions_info.append(reaction_info)
            for comment in comments:
                comment_info = {
                    "id": comment.id,
                    "content": comment.content,
                    "assigned_post": comment.assigned_post.id,
                    "assigned_user": comment.assigned_user.id,
                    "assigned_user_display_name": comment.assigned_user.display_name,
                    "assigned_user_avatar": request.build_absolute_uri(comment.assigned_user.avatar.url),
                    "time": comment.time
                }
                comments_info.append(comment_info)
            info['comments_info'] = comments_info
            info['reactions_info'] = reactions_info
            info['polls_info'] = self.get_poll_info(request, post)
            response_info.append(info)

        def by_id_method(obj):
            return obj['id']
        if params.get('order_by') == ['reversed']:
            response_info.sort(key=by_id_method)
        else:
            response_info.sort(key=by_id_method, reverse=True)
        # print(response_info)
        return Response(response_info)

    def retrieve(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs["pk"])
        user = request.user
        # print(post)
        reactions = Reaction.objects.filter(assigned_post=post)
        comments = Comment.objects.filter(assigned_post=post)
        reactions_info = []
        comments_info = []
        # print(post.photos.all())
        post_info = {
            "assigned_user_id": post.assigned_user.id,
            "assigned_user_avatar":'http://' + request.get_host() + post.assigned_user.avatar.url,
            "assigned_user_display_name": post.assigned_user.display_name,
            "assigned_group_id": post.assigned_group.id,
            "assigned_group_name": post.assigned_group.name,
            "photos": list(map(lambda x: 'http://' + request.get_host() + x.img_url.url, post.photos.all())),
            "content": post.content,
            "time": post.time,
            "type": post.type,
            "reaction_id": Reaction.objects.get(assigned_post=post, assigned_user=user).id if len(Reaction.objects.filter(assigned_post=post, assigned_user=user)) > 0 else -1,
        }
        for reaction in reactions:
            info = {
                "choice": reaction.type,
                "assigned_user": reaction.assigned_user.id,
                "assigned_user_display_name": reaction.assigned_user.display_name,
            }
            reactions_info.append(info)
        for comment in comments:
            info = {
                "id": comment.id,
                "content": comment.content,
                "assigned_post": comment.assigned_post.id,
                "assigned_user": comment.assigned_user.id,
                "assigned_user_display_name": comment.assigned_user.display_name,
                "assigned_user_avatar": request.build_absolute_uri(comment.assigned_user.avatar.url),
                "time": comment.time
            }
            comments_info.append(info)

        return Response(
            {
                "post": post_info,
                "reactions_info": reactions_info,
                "comments_info": comments_info,
                "polls_info": self.get_poll_info(request, post)
            }
        )

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
        post_response = {
                "id": new_post.id,
                "content": new_post.content,
                "assigned_user_id": new_post.assigned_user.id,
                "assigned_user_avatar": 'http://' + request.get_host() + new_post.assigned_user.avatar.url,
                "assigned_user_display_name": new_post.assigned_user.display_name,
                "assigned_group_id": new_post.assigned_group.id,
                "assigned_group_name": new_post.assigned_group.name,
                "reaction_number": 0,
                "comment_number": 0,
                "time": str(new_post.time),
                "type": new_post.type,
                "photos": list(map(lambda x: 'http://' + request.get_host() + x.img_url.url, new_post.photos.all())),
                "reaction_id": -1
            }

        print(post_response)

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
        
        return Response(post_response)

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
        return Response({"reaction_id": new_reaction.id})

    def delete(self, request, *args, **kwargs):
        reaction = Reaction.objects.get(id=kwargs["pk"])
        reaction.delete()
        return Response({"status": "Done"})


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
        new_tick = Tick(users=[user], assigned_poll=Poll.objects.get(id=poll_id))
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
