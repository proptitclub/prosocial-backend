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
        fields = ["url", "id", "name", "description", "members", "admins", "cover"]


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
    assigned_user_display_name = serializers.SerializerMethodField()

    def get_assigned_user_avatar(self, obj):
        request = self.context.get('request')
        
        return request.build_absolute_uri(obj.assigned_user.avatar.url)

    def get_assigned_user_display_name(self, obj):
        return obj.assigned_user.display_name
    


    class Meta:
        model = Comment
        fields = ["url", "id", "content", "assigned_post", "assigned_user", "assigned_user_avatar", "assigned_user_display_name"]


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ["url", "id", "assigned_user", "assigned_post", "type"]


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
        fields = ["url", "id", "assigned_post", "question", "ticks"]


class TickSerializer(serializers.ModelSerializer):
    users = CustomMemberSerializer(many=True)

    class Meta:
        model = Tick
        fields = ["url", "id", "assigned_poll", "users"]
