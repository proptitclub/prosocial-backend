from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Member, GroupPro, Post, Comment, Reaction, Poll, Tick


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


class MemberSerializer(serializers.ModelSerializer):
    assigned_user = UserSerializer()

    class Meta:
        model = Member
        fields = ["assigned_user", "display_name"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    members = MemberSerializer(many=True)
    admins = MemberSerializer(many=True)

    class Meta:
        model = GroupPro
        fields = ("members", "admins")


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "content", "time", "type"]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content", "assigned_post", "assigned_user"]


class ReactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reaction
        fields = ["id"]


class PollSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Poll
        fields = ["id"]


class TickSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tick
        fields = ["id"]
