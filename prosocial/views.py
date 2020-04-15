from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    # UserSerializer,
    # MemberSerializer,
    GroupSerializer,
    PostSerializer,
    CommentSerializer,
    ReactionSerializer,
    PollSerializer,
    TickSerializer,
    CustomMemberSerializer
)

from .models import GroupPro, Post, Comment, Reaction, Poll, Tick, CustomMember


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
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


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ReactionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer


class PollViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class TickViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Tick.objects.all()
    serializer_class = TickSerializer

# custom TokenObtain view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # print(user)
        token = super().get_token(user)
        # print(type(token))
        token['id'] = user.id
        # print(token)
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer