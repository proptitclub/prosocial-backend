from django.contrib.auth.models import User

from rest_framework import serializers

from .models import *

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ["url", "username", "email", "is_staff"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMember
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomMember(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomMemberSerializer(serializers.ModelSerializer):
    participating_group = serializers.SerializerMethodField()

    def get_participating_group(self, obj):
        request = self.context.get('request')
        result_set = (GroupPro.objects.filter(members__in=[obj]) | GroupPro.objects.filter(admins__in=[obj])).distinct()
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
            "first_name",
            "last_name",
            "is_staff",
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
            "cover",
        ]

class CreateGroupSerializer(serializers.ModelSerializer):
    cover = serializers.FileField()
    
    class Meta:
        model = GroupPro
        fields = [
            "members",
            "admins",
            "name",
            "description",
            "members",
            "cover",
        ]
    
    def create(self, validated_data):
        user = self.context.get('request').user
        instance = GroupPro(**validated_data)
        instance.admins.add(user)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == 'members':
                member_list = CustomMember.objects.filter(id__in=value)
                instance.update(members=member_list)
            elif key == 'admins':
                admin_list = CustomMember.objects.filter(id__in=value)
                instance.update(admins=admin_list)
            else:
                setattr(instance, attr, value)
        
        instance.save()
        return instance


# class PostSerializer(serializers.ModelSerializer):
#     # id = serializers.CharField(source='assigned_user', read_only=True)
#     # username = serializers.CharField(source='assigned_group.id', read_only=True)

#     class Meta:
#         model = Post
#         fields = [
#             "url",
#             "id",
#             "content",
#             "time",
#             "type",
#             "assigned_user",
#             "assigned_group",
#         ]




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
            "time",
        ]

class CommentSummary(serializers.ModelSerializer):
    assigned_user = AssignedUserSummary()

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "assigned_user",
            "time",
        ]


class CreateCommentSerializer(serializers.ModelSerializer):
    assigned_post = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = [
            "assigned_post",
            "content",
            "id",
        ]

class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
    
    def update(self, instance, validated_data):
        content = validated_data.get('content')
        instance.__dict__.update({"content": content})
        instance.save()
        return instance


class ReactionSerializer(serializers.ModelSerializer):
    # assigned_post = serializers.SerializerMethodField()
    assigned_user = AssignedUserSummary()

    def get_assigned_post(self, obj):
        return obj.assigned_post.id
    
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
    assigned_user = AssignedUserSummary()

    class Meta:
        model = Reaction
        fields = [
            "id",
            "type",
            "assigned_user",
        ]


class CreateUpdateReactionSerializer(serializers.ModelSerializer):
    # assigned_post = serializers.IntegerField()

    class Meta:
        model = Reaction
        fields = [
            "id",
            "assigned_post",
            "type",
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
        depth = 1

class PollSummary(serializers.ModelSerializer):
    ticks = serializers.SerializerMethodField()

    def get_ticks(self, obj):
        request = self.context.get('request')
        tick_query = Tick.objects.filter(assigned_poll=obj)
        return TickSummary(tick_query, many=True, context={'request': request}).data
    
    class Meta:
        model = Poll
        fields = [
            "id",
            "question",
            "ticks",
        ]

class CreatePollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = [
            "assigned_post",
            "question",
        ]

class UpdatePollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = [
            'question'
        ]

class TickSerializer(serializers.ModelSerializer):
    assigned_user = AssignedUserSummary()

    class Meta:
        model = Tick
        fields = [
            "url", 
            "id", 
            "assigned_poll", 
            "assigned_user",
        ]

class TickSummary(serializers.ModelSerializer):
    assigned_user = AssignedUserSummary()

    class Meta:
        model = Tick
        fields = [
            "id",
            "assigned_user",
        ]

class CreateTickSerializer(serializers.ModelSerializer):
    poll_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Tick
        fields = [
            "poll_id"
        ]

class AssignedGroupSummary(serializers.ModelSerializer):
    cover = serializers.FileField()
    is_admin = serializers.SerializerMethodField()

    def get_is_admin(self, obj):
        user = self.context.get('request').user
        print(obj.admins)
        if user in obj.admins.all():
            return True
        return False

    class Meta:
        model = GroupPro
        fields = [
            'id',
            'name',
            'cover',
            'is_admin'
        ]

class AssignedPostSummary(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
        ]

class NotificationSerializer(serializers.ModelSerializer):
    assigned_user = AssignedUserSummary()
    assigned_post = AssignedPostSummary()
    assigned_group = serializers.SerializerMethodField()

    def get_assigned_group(self, obj):
        return AssignedGroupSummary(obj.assigned_post.assigned_group, context=self.context).data

    class Meta:
        model = Notification
        fields = [
            "id",
            "assigned_user", 
            "assigned_post", 
            "assigned_group",
            "type",
            "created_time",
        ]
        depth = 1

class NotificationMemberSerializer(serializers.ModelSerializer):
    assigned_notification = NotificationSerializer()

    class Meta:
        model = NotificationMember
        fields = [
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


# class TickSummary(serializers.ModelSerializer):
#     users = AssignedUserSummary(many=True, read_only=True)

#     class Meta:
#         model = Tick
#         fields = [
#             'id',
#             'users'
#         ]

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
    reaction_id = serializers.SerializerMethodField()

    def get_reaction_number(self, obj):
        return len(Reaction.objects.filter(assigned_post=obj))
    
    def get_comment_number(self, obj):
        return len(Comment.objects.filter(assigned_post=obj))
    
    def get_reactions(self, obj):
        request = self.context.get('request')
        reactions = Reaction.objects.filter(assigned_post=obj)
        filtered_reactions = []
        blocked_users = MemberSpecialRelationship.objects.filter(owner=request.user, relation_type=0)
        blocked_users_id = []

        for blocked_user in blocked_users:
            blocked_users_id.append(blocked_user.another.id)
        
        for comment in reactions:
            if comment.assigned_user.id in blocked_users_id:
                continue
            else:
                filtered_reactions.append(comment)
        return ReactionSerializerSummary(filtered_reactions, many=True, context={'request': request}).data
    
    def get_polls(self, obj):
        request = self.context.get('request')
        return PollSummary(Poll.objects.filter(assigned_post=obj), many=True, context={'request':request}).data

    def get_reaction_id(self, obj):
        request = self.context.get('request')
        user = request.user
        try:
            reaction = Reaction.objects.filter(assigned_post=obj, assigned_user=user)[0]
            print(reaction)
            return reaction.id
        except:
            return -1

    class Meta:
        model = Post
        fields = [
            'id', # in post model
            'content', # in post model
            'assigned_user',
            'assigned_group',
            'reaction_number',
            'comment_number',
            'time',
            'update_time', # in post model
            'type', # in ,post model
            'photos',
            'reactions',
            'polls',
            'reaction_id',
        ]

class CreatePostSerializer(serializers.ModelSerializer):
    def get_comment_number(self, obj):
        return 0
    class Meta:
        model = Post
        fields = [
            'id',
            'content',
            'assigned_user',
            'assigned_group',
            'type',
            'photos',
            'polls',
            'comment_number'
        ]

class PostSerializer(serializers.ModelSerializer):
    assigned_user = AssignedUserSummary()
    assigned_group = AssignedGroupSummary()
    comments = serializers.SerializerMethodField(read_only=True)
    photos = ImageSerializer(many=True)
    polls = serializers.SerializerMethodField()
    reaction_id = serializers.SerializerMethodField()
    reaction_number = serializers.SerializerMethodField()

    
    def get_comments(self, obj):
        request = self.context.get('request')
        comments = Comment.objects.filter(assigned_post=obj)
        filtered_comments = []
        blocked_users = MemberSpecialRelationship.objects.filter(owner=request.user, relation_type=0)
        blocked_users_id = []

        for blocked_user in blocked_users:
            blocked_users_id.append(blocked_user.another.id)
        
        for comment in comments:
            if comment.assigned_user.id in blocked_users_id:
                continue
            else:
                filtered_comments.append(comment)
        return CommentSummary(filtered_comments, many=True, context={'request': request}).data
    
    def get_polls(self, obj):
        request = self.context.get('request')
        return PollSummary(Poll.objects.filter(assigned_post=obj), many=True, context={'request':request}).data

    def get_reaction_id(self, obj):
        request = self.context.get('request')
        user = request.user
        try:
            reaction = Reaction.objects.filter(assigned_post=obj, assigned_user=user)[0]
            print(reaction)
            return reaction.id
        except:
            return -1

    def get_reaction_number(self, obj):
        request = self.context.get('request')
        reactions = Reaction.objects.filter(assigned_post=obj)
        return len(reactions)
    


    class Meta:
        model = Post
        fields = [
            'id', # in post model
            'content', # in post model
            'assigned_user',
            'assigned_group',
            'comments',
            'time',
            'update_time', # in post model
            'type', # in post model
            'photos',
            'polls',
            'reaction_id',
            'reaction_number',
        ]

class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'content',
        ]

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = "__all__"

class CreatePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = [
            'score',
            'description'
        ]

class TargetSerializer(serializers.ModelSerializer):
    assigned_user = AssignedUserSummary(read_only=True)
    point = PointSerializer(read_only=True)

    class Meta:
        model = Target
        fields = [
            "id",
            "assigned_user",
            "name",
            "is_done",
            "point",
            "status",
            "created_time",
            "result_image"
        ]

class CreateTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = [
            "name",
            "point",
        ]

    def create(self, validated_data):
        assigned_user = self.context['request'].user
        name = validated_data.get('name')
        
        instance = Target(assigned_user=assigned_user, name=name)
        instance.save()
        return instance

class UpdateTargetSerializer(serializers.ModelSerializer):
    point = serializers.IntegerField()
    
    class Meta:
        model = Target
        fields = [
            "name",
            "is_done",
            "point",
            "status",
            "result_image"
        ]

    # def update(self, instance, validated_data):
    #     name = validated_data.get('name')
    #     is_done = validated_data.get('is_done')
    #     point = Point.objects.get(id=validated_data.get('point'))
    #     status = validated_data.get('status')
    #     result_image = validated_data.get()

    #     instance.__dict__.update(
    #         {
    #             'name': name,
    #             'is_done': is_done,
    #             'point': point,
    #             'status': status
    #         }
    #     )
    #     instance.save()
    #     return instance

class BonusPointSerializer(serializers.ModelSerializer):
    assigned_user = AssignedUserSummary(read_only=True)

    class Meta:
        model = BonusPoint
        fields = [
            "assigned_user",
            "score",
            "description",
            "created_time",
        ]

class CreateBonusPointSerializer(serializers.ModelSerializer):
    assigned_user = serializers.IntegerField()
    class Meta:
        model = BonusPoint
        fields = [
            "assigned_user",
            "score",
            "description",
        ]
    
    def create(self, validated_data):
        assigned_user = CustomMember.objects.get(id=assigned_user)
        score = validated_data.get('score')
        description = validated_data.get('description')

        instance = BonusPoint(assigned_user=assigned_user, score=score, description=description)
        instance.save()
        return instance
    
class UpdateBonusPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusPoint
        fields = [
            "score",
            "description",
        ]

    def update(self, instance, validated_data):
        score = validated_data.get('score')
        description = validated_data.get('description')
        instance.__dict__.update({
            'score': score,
            'description': description,
        })
        instance.save()
        return instance


class CreateUserSerializer(serializers.Serializer):
    class Meta:
        model = CustomMember
        fields = [
            "username",
            "password",
        ]
