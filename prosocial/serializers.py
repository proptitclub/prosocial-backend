from django.contrib.auth.models import User

from rest_framework import serializers

from .models import GroupPro, Post, Comment, Reaction, Poll, Tick, CustomMember

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ["url", "username", "email", "is_staff"]


class CustomMemberSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(source="assigned_user.id", read_only=True)
    # username = serializers.CharField(source="assigned_user.username", read_only=True)
    participating_group = serializers.SerializerMethodField()

    def get_participating_group(self, obj):
        return GroupPro.objects.filter(members=obj).values("id")

    class Meta:
        model = CustomMember
        fields = [
            "avatar",
            "url",
            "id",
            "username",
            "display_name",
            "phone_number",
            "facebook",
            "role",
            "date_of_birth",
            "description",
            "email",
            "participating_group",
        ]

    def create(self, validated_data):
        validated_data["validate_data"] = False


# class MemberSerializer(serializers.ModelSerializer):
#     # id = serializers.CharField(source="assigned_user.id", read_only=True)
#     # username = serializers.CharField(source="assigned_user.username", read_only=True)

#     class Meta:
#         model = Member
#         fields = [
#             "url",
#             "id",
#             "username",
#             "display_name",
#             "phone_number",
#             "facebook",
#             "role",
#             "date_of_birth",
#             "description",
#             "email",
#         ]

#     def create(self, validated_data):
#         validated_data["validate_data"] = False


class GroupSerializer(serializers.ModelSerializer):
    members = CustomMemberSerializer(many=True)
    admins = CustomMemberSerializer(many=True)

    class Meta:
        model = GroupPro
        fields = ["url", "id", "name", "description", "members", "admins"]


class PostSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(source='assigned_user', read_only=True)
    # username = serializers.CharField(source='assigned_group.id', read_only=True)

    class Meta:
        model = Post
        fields = [
            "url",
            "id",
            "content",
            "time",
            "type",
            "assigned_user",
            "assigned_group",
        ]


class CommentSerializer(serializers.ModelSerializer):
    assigned_user_avatar = serializers.SerializerMethodField()

    def get_assigned_user_avatar(self, obj):
        request = self.context.get('request')
        
        return request.build_absolute_uri(obj.assigned_user.avatar.url)

    class Meta:
        model = Comment
        fields = ["url", "id", "content", "assigned_post", "assigned_user", "assigned_user_avatar"]


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ["url", "id", "assigned_user", "assigned_post", "type"]


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ["url", "id", "assigned_post", "question"]


class TickSerializer(serializers.ModelSerializer):
    users = CustomMemberSerializer(many=True)

    class Meta:
        model = Tick
        fields = ["url", "id", "assigned_poll", "users", "answer"]
