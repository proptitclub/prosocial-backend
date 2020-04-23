from abc import ABC

from django.contrib.auth.models import User
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
from .models import GroupPro, Post, Comment, Reaction, Poll, Tick, CustomMember, Image

# custom TokenObtain view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = CustomMember.objects.all()
    serializer_class = CustomMemberSerializer


# class AccountViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = Member.objects.all()
#     serializer_class = MemberSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = GroupPro.objects.all()
    serializer_class = GroupSerializer

    def retrieve(self, request, *args, **kwargs):
        group = GroupPro.objects.get(id=kwargs["pk"])
        groups_info = []
        posts = Post.objects.filter(assigned_group=group)
        for post in posts:
            post_info = {
                "assigned_user": post.assigned_user,
                "content": post.content,
                "time": post.time,
                "type": post.type,
            }
            posts_info.append(post_info)

        info = {
            "name": group.name,
            "description": group.description,
            "admins": group.admins,
            "members": group.members,
            "posts": posts_info,
        }
        return Response({"group": info})


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        posts = Post.objects.all()
        response_info = []

        for post in posts:
            print(post.assigned_user.avatar)
            info = {
                "id": post.id,
                "content": post.content,
                "assigned_user_id": post.assigned_user.id,
                "assigned_user_avatar": post.assigned_user.avatar.url,
                "assigned_user_display_name": post.assigned_user.display_name,
                "assigned_group_id": post.assigned_group.id,
                "assigned_group_name": post.assigned_group.name,
                "reaction_number": len(Reaction.objects.filter(assigned_post=post)),
                "comment_number": len(Reaction.objects.filter(assigned_post=post)),
                "time": post.time,
                "type": post.type,
                "photos": list(map(lambda x: x.img_url.url, post.photos.all()))
            }
            response_info.append(info)
            # print(response_info)
        return Response(response_info)

    def retrieve(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs["pk"])
        # print(post)
        reactions = Reaction.objects.filter(assigned_post=post)
        comments = Comment.objects.filter(assigned_post=post)
        reactions_info = []
        comments_info = []
        # print(post.photos.all())
        post_info = {
            "assigned_user_id": post.assigned_user.id,
            "assigned_user_avatar": post.assigned_user.avatar.url,
            "assigned_user_display_name": post.assigned_user.display_name,
            "assigned_group_id": post.assigned_group.id,
            "assigned_group_name": post.assigned_group.name,
            "photos": list(map(lambda x: x.img_url.url, post.photos.all())),
            "content": post.content,
            "time": post.time,
            "type": post.type,
        }
        for reaction in reactions:
            info = {
                "choice": reaction.type,
                "assigned_user": reaction.assigned_user.id,
                "assigned_username": reaction.assigned_user.username,
            }
            reactions_info.append(info)
        for comment in comments:
            info = {
                "content": comment.content,
                "assigned_user": comment.assigned_user.id,
                "assigned_username": comment.assigned_user.username,
            }
            comments_info.append(info)

        return Response(
            {
                "post": post_info,
                "reactions_info": reactions_info,
                "comments_info": comments_info,
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


        return Response({"status": "DONE"})

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
        return Response({"status": "Done"})

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
