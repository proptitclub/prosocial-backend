from django.contrib.auth.models import User
from rest_framework import viewsets

from .serializers import (
    UserSerializer,
    MemberSerializer,
    GroupSerializer,
    PostSerializer,
    CommentSerializer,
    ReactionSerializer,
    PollSerializer,
    TickSerializer,
)

from .models import Member, GroupPro, Post, Comment, Reaction, Poll, Tick


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = GroupPro.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class TickViewSet(viewsets.ModelViewSet):
    queryset = Tick.objects.all()
    serializer_class = TickSerializer
