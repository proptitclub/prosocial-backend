from django.contrib.auth.models import User

from rest_framework import serializers

from .models import *

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ["url", "username", "email", "is_staff"]


class CustomMemberSerializer(serializers.ModelSerializer):
    participating_group = serializers.SerializerMethodField()

    def get_participating_group(self, obj):
        request = self.context.get('request')
        result_set = GroupPro.objects.filter(members=obj)
        return AssignedGroupSummary(result_set, many=True, context={"request": request}).data
        

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
            "user_gender",
            "cover",
            "class_name",
        ]

    def create(self, validated_data):
        validated_data["validate_data"] = False


class AssignedUserSummary(serializers.ModelSerializer):
    avatar = serializers.FileField()

    class Meta:
        model = CustomMember
        fields = [
            'id',
            'avatar',
            'display_name'
        ]

class GroupSerializer(serializers.ModelSerializer):
    cover = serializers.FileField()
    members = AssignedUserSummary(many=True)
    admins = AssignedUserSummary(many=True)

    class Meta:
        model = GroupPro
        fields = [
            "url", 
            "id", 
            "name", 
            "description", 
            "members", 
            "admins", 
            "cover"
        ]


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
    assigned_user = AssignedUserSummary()


    class Meta:
        model = Comment
        fields = [
            "url", 
            "id", 
            "content", 
            "assigned_post", 
            "assigned_user",
        ]

class CommentSummary(serializers.ModelSerializer):
    assigned_user = AssignedUserSummary()

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "assigned_user",
        ]


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = [
            "url", 
            "id", 
            "assigned_user", 
            "assigned_post", 
            "type",
        ]

class ReactionSummary(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = [
            "id",
            "type",
            "assigned_user",
        ]



class TickSerializer(serializers.ModelSerializer):
    users = AssignedUserSummary(read_only=True)
    
    class Meta:
        model = Tick
        fields = [
            'id',
            'user',
            'assigned_poll',
        ]




class PollSerializer(serializers.ModelSerializer):
    ticks = serializers.SerializerMethodField()

    def get_ticks(self, obj):
        request = self.context.get('request')
        tick_query = Tick.objects.filter(assigned_poll=obj)
        return TickSummary(tick_query, many=True, context={'request':request}).data

    class Meta:
        model = Poll
        fields = [
            "url", 
            "id", 
            "assigned_post", 
            "question", 
            "ticks",
        ]


class TickSerializer(serializers.ModelSerializer):
    users = AssignedUserSummary(many=True)

    class Meta:
        model = Tick
        fields = [
            "url", 
            "id", 
            "assigned_poll", 
            "users",
        ]

class TickSummary(serializers.ModelSerializer):
    user = AssignedUserSummary()

    class Meta:
        model = Tick
        fields = [
            "id",
            "user",
        ]



class AssignedGroupSummary(serializers.ModelSerializer):
    cover = serializers.FileField()

    class Meta:
        model = GroupPro
        fields = [
            'id',
            'name',
            'cover',
        ]

class AssignedPostSummary(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
        ]

class NotificationSerializer(serializers.ModelSerializer):
    assigned_user = AssignedUserSummary(read_only=True)
    assigned_post = AssignedPostSummary(read_only=True)
    assigned_group = serializers.SerializerMethodField()

    def get_assigned_group(self, obj):
        return AssignedGroupSummary(obj.assigned_post.assigned_group).data

    class Meta:
        model = Notification
        fields = [
            "assigned_user", 
            "assigned_post", 
            "assigned_group",
            "type",
            "created_time",
        ]
        depth = 1

class NotificationMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationMember
        fields = [
            "assigned_user",
            "assigned_notification",
            "is_seen",
        ]


class ImageSerializer(serializers.ModelSerializer):
    img_url = serializers.FileField()

    class Meta:
        model = Image
        fields = [
            "id",
            "img_url",
        ]


class TickSummary(serializers.ModelSerializer):
    users = AssignedUserSummary(many=True, read_only=True)

    class Meta:
        model = Tick
        fields = [
            'id',
            'users'
        ]

class ReactionSerializerSummary(serializers.ModelSerializer):
    assigned_user = AssignedUserSummary()

    class Meta:
        model = Reaction
        fields = [
            'id',
            'type',
            'assigned_user'
        ]
        depth = 1


class PostSummary(serializers.ModelSerializer):
    assigned_user = AssignedUserSummary()
    assigned_group = AssignedGroupSummary()
    reaction_number = serializers.SerializerMethodField()
    comment_number = serializers.SerializerMethodField()
    photos = ImageSerializer(many=True, read_only=True)
    reactions = serializers.SerializerMethodField()
    polls = serializers.SerializerMethodField()

    def get_reaction_number(self, obj):
        return len(Reaction.objects.filter(assigned_post=obj))
    
    def get_comment_number(self, obj):
        return len(Comment.objects.filter(assigned_post=obj))
    
    def get_reactions(self, obj):
        request = self.context.get('request')
        return ReactionSerializerSummary(Reaction.objects.filter(assigned_post=obj), many=True, context={'request': request}).data
    
    def get_polls(self, obj):
        request = self.context.get('request')
        return PollSerializer(Poll.objects.filter(assigned_post=obj), many=True, context={'request':request}).data


    class Meta:
        model = Post
        fields = [
            'id', # in post model
            'content', # in post model
            'assigned_user',
            'assigned_group',
            'reaction_number',
            'comment_number',
            'time', # in post model
            'type', # in post model
            'photos',
            'reactions',
            'polls',
        ]

class PostSerializer(serializers.ModelSerializer):
    assigned_user = AssignedUserSummary()
    assigned_group = AssignedGroupSummary()
    comments = serializers.SerializerMethodField()
    photos = ImageSerializer(many=True, read_only=True)
    reactions = serializers.SerializerMethodField()
    polls = serializers.SerializerMethodField()

    
    def get_comments(self, obj):
        request = self.context.get('request')
        return CommentSummary(Comment.objects.filter(assigned_post=obj), many=True, context={'request': request}).data
    
    
    def get_reactions(self, obj):
        request = self.context.get('request')
        return ReactionSerializerSummary(Reaction.objects.filter(assigned_post=obj), many=True, context={'request': request}).data
    
    def get_polls(self, obj):
        request = self.context.get('request')
        return PollSerializer(Poll.objects.filter(assigned_post=obj), many=True, context={'request':request}).data


    class Meta:
        model = Post
        fields = [
            'id', # in post model
            'content', # in post model
            'assigned_user',
            'assigned_group',
            'comments',
            'time', # in post model
            'type', # in post model
            'photos',
            'reactions',
            'polls',
        ]