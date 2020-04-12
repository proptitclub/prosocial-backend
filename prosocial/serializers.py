from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Member, GroupPro, Post, Comment, Reaction, Poll, Tick


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


class MemberSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='assigned_user.id', read_only=True)
    username = serializers.CharField(source='assigned_user.username', read_only=True)

    class Meta:
        model = Member
        fields = ["url", "id", "username", "display_name", "phone_number", "facebook", "role", "date_of_birth",
                  "description", "email"]

    def create(self, validated_data):
        validated_data["validate_data"] = False


class GroupSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)
    admins = MemberSerializer(many=True)

    class Meta:
        model = GroupPro
        fields = ["url", "id", "name", "description", "members", "admins"]


class PostSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(source='assigned_user', read_only=True)
    # username = serializers.CharField(source='assigned_group.id', read_only=True)

    class Meta:
        model = Post
        fields = ["url", "id", "content", "time", "type", "assigned_user", "assigned_group"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["url", "id", "content", "assigned_post", "assigned_user"]


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ["url", "id", "assigned_user", "assigned_post", "type"]


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ["url", "id", "assigned_post", "question"]


class TickSerializer(serializers.ModelSerializer):
    users = MemberSerializer(many=True)

    class Meta:
        model = Tick
        fields = ["url", "id", "assigned_poll", "users", "answer"]
