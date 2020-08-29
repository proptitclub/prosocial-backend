from django.contrib.auth.models import User

from rest_framework import serializers

from .models import *

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ["url", "username", "email", "is_staff"]


class CustomMemberSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(source="assigned_user.id", read_only=True)
    # username = serializers.CharField(source="assigned_user.username", read_only=True)
    participating_group = serializers.SerializerMethodField()

    def get_participating_group(self, obj):
        result_set = GroupPro.objects.filter(members=obj).values("id", "cover", "name")
        # result_set = GroupPro.objects.filter(members=obj)
        group_admin_set = GroupPro.objects.filter(admins=obj)
        response_list = list()
        for result in result_set:
            response = dict(result)
            response['is_admin'] = False
            for group_obj in group_admin_set:
                if group_obj.id == response['id']:
                    response['is_admin'] = True
            response['cover'] = "http://103.130.218.26:6960/media/" + result['cover']
            response_list.append(response)
        # return id, "http://103.130.218.26:6960/media/" + cover, name
        return response_list
        

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


class GroupSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    admins = serializers.SerializerMethodField()
    def get_cover(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.cover.url)

    def get_members(self, obj):
        request = self.context.get('request')
        members = list(obj.members.all())
        
        members_info = []
        for member in members:
            user_info = {}
            user_info['avatar'] = request.build_absolute_uri(member.avatar.url)
            user_info['display_name'] = member.display_name
            user_info['id'] = member.id
            members_info.append(user_info)
        return members_info

    def get_admins(self, obj):
        request = self.context.get('request')
        admins = list(obj.admins.all())
        
        admins_info = []
        for member in admins:
            user_info = {}
            user_info['avatar'] = request.build_absolute_uri(member.avatar.url)
            user_info['display_name'] = member.display_name
            user_info['id'] = member.id
            admins_info.append(user_info)
        return admins_info

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

class AssignedUserSummary(serializers.ModelSerializer):
    avatar = serializers.FileField()

    def get_avatar(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.avatar.url)

    class Meta:
        model = CustomMember
        fields = [
            'id',
            'avatar',
            'display_name'
        ]


class CommentSerializer(serializers.ModelSerializer):
    assigned_user_avatar = serializers.SerializerMethodField()
    assigned_user_display_name = serializers.SerializerMethodField()

    def get_assigned_user_avatar(self, obj):
        request = self.context.get('request')
        
        return request.build_absolute_uri(obj.assigned_user.avatar.url)

    def get_assigned_user_display_name(self, obj):
        return obj.assigned_user.display_name
    


    class Meta:
        model = Comment
        fields = [
            "url", 
            "id", 
            "content", 
            "assigned_post", 
            "assigned_user", 
            "assigned_user_avatar", 
            "assigned_user_display_name",
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



class TickSerializer(serializers.ModelSerializer):
    users = AssignedUserSummary(many=True, read_only=True)
    
    class Meta:
        model = Tick
        fields = [
            'id',
            'users',
            'assigned_poll',
        ]




class PollSerializer(serializers.ModelSerializer):
    ticks = serializers.SerializerMethodField()
    

    def get_ticks(self, obj):
        request = self.context.get('request')
        ticks = Tick.objects.filter(assigned_poll=obj).values('users')
        
        ticks_info = []
        for user_id in ticks:
            user = CustomMember.objects.get(id=user_id.get('users'))
            user_info = {}
            user_info['avatar'] = request.build_absolute_uri(user.avatar.url)
            user_info['display_name'] = user.display_name
            user_info['id'] = user.id
            ticks_info.append(user_info)
        return ticks_info

    class Meta:
        model = Poll
        fields = [
            "url", 
            "id", 
            "assigned_post", 
            "question", 
            "ticks"
        ]


class TickSerializer(serializers.ModelSerializer):
    users = CustomMemberSerializer(many=True)

    class Meta:
        model = Tick
        fields = [
            "url", 
            "id", 
            "assigned_poll", 
            "users"
        ]




class AssignedGroupSummary(serializers.ModelSerializer):
    class Meta:
        model = GroupPro
        fields = [
            'id',
            'name'
        ]

class AssignedPostSummary(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id'
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
    img_url = serializers.SerializerMethodField()
    def get_img_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.img_url.url)

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


class PostSerializer(serializers.ModelSerializer):
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
        return ReactionSerializerSummary(Reaction.objects.filter(assigned_post=obj), many=True).data
    
    def get_polls(self, obj):
        return PollSerializer(Poll.objects.filter(assigned_post=obj), many=True).data


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