from abc import ABC

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, DjangoMultiPartParser, JSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer
from .serializers import *
from datetime import datetime
from .models import *
from django.db.models import QuerySet
# custom TokenObtain view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
import requests
import json
from .notification_sender import *
from rest_framework.decorators import action, api_view, permission_classes, parser_classes, renderer_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from .pagination import SmallResultSetPagination
from django.http import JsonResponse




APP_ID = '913dba2c-9869-4355-a68e-5be7321465c9'
REST_API_ONESIGNAL_ID = 'ZDg4NTNmNmItYzYxNi00ZjhiLWJmYmQtM2RiOGQ2ZjJhN2Iy'

def send_to_onesignal_worker(app_id, include_player_ids, contents):
    header = {"Content-Type": "application/json; charset=utf-8"}

    payload = {"app_id": app_id,
            "include_player_ids": include_player_ids,
            "contents": {"vi": contents}}
    
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
    
    print(req.status_code, req.reason)


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = CustomMember.objects.all()
    serializer_class = CustomMemberSerializer


# class AccountViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = Member.objects.all()
#     serializer_class = MemberSerializer


class GroupViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = GroupPro.objects.all()
    serializer_class = GroupSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateGroupSerializer
        else:
            return GroupSerializer

    @swagger_auto_schema(responses={'200': openapi.Response('Response Description', GroupSerializer)})
    @parser_classes((MultiPartParser, ))
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    @swagger_auto_schema(responses={'200': openapi.Response('Response Description', GroupSerializer)})
    def update(self, *args, **kwargs):
        return super().create(*args, **kwagrs)


class PostViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = SmallResultSetPagination
    # parser_classes = (FormParser, )

    def get_serializer_class(self):
        if self.action == 'list':
            return PostSummary
        if self.action == 'retrieve':
            return PostSerializer
        if self.action == 'update':
            return UpdatePostSerializer
        return PostSerializer

    def get_queryset(self):
        request = self.request
        user = request.user
        posts = Post.objects.all().order_by('-time')
        filtered_posts = posts
        response_info = []
        params = dict(request.query_params)
        method = params.get('method')
        # print(method)
        if method is not None:
            if method[0] == 'byUser':
                user = CustomMember.objects.get(id=params.get('id')[0])
                filtered_posts = Post.objects.filter(assigned_user=user).order_by('-time')
            if method[0] == 'byGroup':
                group = GroupPro.objects.get(id=params.get('id')[0])
                filtered_posts = Post.objects.filter(assigned_group=group).order_by('-time')

        return filtered_posts
    
    @action(detail=False, methods=['get'], url_path='by_user/(?P<user_id>[^/.]+)')
    def by_user(self, request, user_id, pk=None):
        user = CustomMember.objects.get(id=user_id)
        query_set = Post.objects.filter(assigned_user=user)
        print(query_set)
        return Response(PostSerializer(query_set, many=True, context={'request': request}).data)

    @action(detail=False, methods=['get'], url_path='by_group/(?P<group_id>[^/.]+)')
    def by_group(self, request, group_id, pk=None):
        group = GroupPro.objects.get(id=group_id)
        query_set = Post.objects.filter(assigned_group=group)
        print(query_set)

        return Response(PostSerializer(query_set, many=True, context={'request': request}).data)
    
    @swagger_auto_schema(
        operation_description="Only update content of Post",
        responses={'200': openapi.Response('Response Description', PostSerializer)},
    )
    def update(self, request, *args, **kwargs):
        user = request.user
        post = Post.objects.get(id=kwargs["pk"])
        content = request.data.get("content")
        time_update = datetime.now()
        post.__dict__.update({"content": content})
        post.__dict__.update({"time": time_update})
        post.save()

        return Response(PostSerializer(post, context={'request': request}).data)

    def create(self, request, *args, **kwargs):
        # print(request.method)
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
        count_ = 0
        for count, x in enumerate(request.FILES.getlist("files")):

            def process(f):
                image = Image(img_url=f)
                image.save()
                new_post.photos.add(image)
            count_ = count
            process(x)
        # print(count)

        new_post.save()


        CreatingPostSender.create_noti(request, new_post)
        # new_notification = Notification(
        #     assigned_post=new_post,
        #     assigned_user=request.user,
        #     type=0
        # )
        # new_notification.save()
        # user_list = new_post.assigned_group.members
        if int(new_post.type) == 1:
            polls = request.data.get('polls')
            print(polls)
            if polls == None:
                polls = '{}'
            # print(polls)
            dict_poll_data = json.loads(polls)
            print(dict_poll_data)
            for poll_data in dict_poll_data:
                content = poll_data
                new_poll = Poll(assigned_post=new_post, question=content)
                new_poll.save()
        
        # relation_device_id_list = []
        # for user in user_list.all():
        #     print('{} == {}'.format(user.id, request.user.id))
        #     if user.id == request.user.id:
        #         continue
        #     new_notification_member = NotificationMember(assigned_user=user, assigned_notification=new_notification)
        #     new_notification_member.save()
        #     user_device_list = UserDevice.objects.filter(assigned_user=user)
        #     for user_device in user_device_list:
        #         relation_device_id_list.append(user_device.device_id)
        
        # send_to_onesignal_worker(APP_ID, relation_device_id_list, 'Đây là notification từ post {}'.format(new_post.id))
        
        return Response(PostSerializer(new_post, context={'request': request}).data)

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

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateCommentSerializer
        elif self.action == 'update':
            return UpdateCommentSerializer
        else:
            return CommentSerializer

    def get_queryset(self):
        super().get_queryset()
        # print("it reached here" + "!"*10)
        # print(self.kwargs)
        post_id = self.request.query_params.get('post_id', None)
        if post_id != None:
            post = Post.objects.get(id=post_id)
            return Comment.objects.filter(assigned_post=post)
        else:
            return Comment.objects.all()

    @swagger_auto_schema(responses={'200': openapi.Response('Response Description', CommentSerializer)})
    @parser_classes((MultiPartParser, JSONParser))
    def update(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=kwargs["pk"])
        content = request.data.get("content")

        comment.__dict__.update({"content": content})
        comment.save()
        return Response(CommentSerializer(comment, context={'request': request}).data)


    @swagger_auto_schema(responses={'200': openapi.Response('Response Description', CommentSerializer)})
    @parser_classes((MultiPartParser, JSONParser))
    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data.get("assigned_post")
        post = Post.objects.get(id=post_id)
        content = request.data.get("content")
        new_comment = Comment(assigned_user=user, assigned_post=post, content=content)
        new_comment.save()
        return Response(CommentSerializer(comment, context={'request': request}).data)

    def delete(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=kwargs["pk"])
        comment.delete()
        return Response({"status": "Done"})


class ReactionViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CreateUpdateReactionSerializer
        else:
            return ReactionSerializer

    def get_queryset(self):
        super().get_queryset()
        request = self.request
        user = self.request.user
        params = dict(request.query_params)
        post_id = params.get('postId')
        query_set = Reaction.objects.all()
        # print(method)
        if post_id is not None:
            if post_id[0] != '':
                post_id_num = int(post_id[0])
                print(post_id_num)
                post = Post.objects.get(id=post_id_num)
                query_set = Reaction.objects.filter(assigned_post=post)
        return query_set

    
    @swagger_auto_schema(responses={'200': openapi.Response('Response Description', ReactionSerializer)})
    @parser_classes((MultiPartParser, JSONParser))
    def update(self, request, *args, **kwargs):
        reaction = Reaction.objects.get(id=kwargs["pk"])
        content = request.data.get("type")

        reaction.__dict__.update({"type": content})
        reaction.save()
        return Response(ReactionSerializer(obj, context={'request': request}).data)


    @swagger_auto_schema(responses={'200': openapi.Response('Response Description', ReactionSerializer)})
    @parser_classes((MultiPartParser, JSONParser))
    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data.get("assigned_post")
        post = Post.objects.get(id=post_id)
        content = request.data.get("type")
        new_reaction = Reaction(assigned_user=user, assigned_post=post, type=content)
        new_reaction.save()
        ReactionSender.create_noti(request, new_reaction)
        return Response(ReactionSerializer(new_reaction, context={'request': request}).data)


    @swagger_auto_schema(operation_description='List reactions, if you want to list by post, add "?postId=<post_id>"')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, pk=None):
        # print(pk)
        obj = Reaction.objects.get(id=pk)
        return Response(ReactionSerializer(obj, context={'request': request}).data)
        # return super().retrieve(request, pk)

    def destroy(self, request, pk=None):
        obj = Reaction.objects.get(id=int(pk))
        obj.delete()
        return Response({"detail": True})

class PollViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePollSerializer
        elif self.action == 'update':
            return UpdatePollSerializer
        else:
            return PollSerializer
    
    @swagger_auto_schema(responses={'200': openapi.Response('Response Description', PollSerializer)})
    @parser_classes((MultiPartParser, JSONParser))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={'200': openapi.Response('Response Description', PollSerializer)})
    @parser_classes((MultiPartParser, JSONParser))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)



class TickViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Tick.objects.all()
    serializer_class = TickSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTickSerializer
        else:
            return TickSerializer

    @swagger_auto_schema(responses={'200': openapi.Response('Response Description', TickSerializer)})
    @parser_classes((MultiPartParser, JSONParser))
    def create(self, request, *args, **kwargs):
        user = request.user
        poll_id = request.data.get('assigned_poll')
        new_tick = Tick(assigned_user=user, assigned_poll=Poll.objects.get(id=poll_id))
        new_tick.save()
        return Response(TickSerializer(new_tick, context={'request': request}).data)

# class CommentViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

#     def get_serializer_class(self):
#         if self.action == 'create':
#             return CreateCommentSerializer
#         else:
#             return CommentSerializer

#     @swagger_auto_schema(responses={'200': openapi.Response('Response Description', CommentSerializer)})
#     @parser_classes((MultiPartParser, JSONParser))
#     def create(self, request, *args, **kawrgs):
#         user = request.user
#         content = request.data.get('content')
#         post_id = request.data.get('assigned_post')
#         assigned_post = Post.objects.get(id=post_id)
#         instance = Comment(assigned_user=user, assigned_post=assigned_post, content=content)
#         instance.save()
#         return Response(CommentSerializer(instance, context={'request': request}).data)
    

#     @swagger_auto_schema(responses={'200': openapi.Response('Response Description', CommentSerializer)})
#     @parser_classes((MultiPartParser, JSONParser))
#     def update(self, request, pk):
#         content = request.data.get('content')
#         instance = Comment.objects.get(id=pk)
#         instance.update



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



class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(assigned_user=user).order_by('-created_time')


class NotificationMemberViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationMemberSerializer

    def get_queryset(self):
        user = self.request.user
        return NotificationMember.objects.filter(assigned_user=user)

class NewsFeedViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSummary
    pagination_class = SmallResultSetPagination

    def get_queryset(self):
        user = self.request.user
        attended_group_as_member = GroupPro.objects.filter(members__in=[user])
        attended_group_as_admin = GroupPro.objects.filter(admins__in=[user])
        attended_group = (attended_group_as_admin | attended_group_as_member).distinct()

        list_post = Post.objects.none()
        for group in attended_group:
            list_post = list_post | Post.objects.filter(assigned_group=group)
        list_post = list_post.distinct()
        list_post = list_post.order_by('-time')
        return list_post

class PointViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PointSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CreatePointSerializer
        else:
            return PointSerializer

    def get_queryset(self):
        return Point.objects.all()

    @swagger_auto_schema(responses={'200': openapi.Response('Response Description', PointSerializer)})
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    @swagger_auto_schema(responses={'200': openapi.Response('Response Description', PointSerializer)})
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

class TargetViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TargetSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTargetSerializer
        elif self.action == 'update':
            return UpdateTargetSerializer
        else:
            return TargetSerializer
    def get_queryset(self):
        request = self.request
        user = self.request.user
        params = dict(request.query_params)
        method = params.get('method')
        query_set = Target.objects.all()
        # print(method)
        if method is not None:
            if method[0] == 'userCurrentMonth':
                cur_month = datetime.today().replace(day=1)
                query_set = Target.objects.filter(created_time__gt=cur_month, assigned_user=user)
            if method[0] == 'currentMonth':
                cur_month = datetime.today().replace(day=1)
                query_set = Target.objects.filter(created_time__gt=cur_month)

        return query_set

    # @swagger_auto_schema(responses={'200': openapi.Response('Response Description', TargetSerializer)})
    # @parser_classes((MultiPartParser, JSONParser))
    # def create(self, *args, **kwargs):
    #     return super().create(*args, **kwargs)
    
    # @swagger_auto_schema(responses={'200': openapi.Response('Response Description', TargetSerializer)})
    # @parser_classes((MultiPartParser, JSONParser))
    # def update(self, *args, **kwargs):
    #     return super().update(*args, **kwargs)

    @swagger_auto_schema(operation_description='If you want to get all Target, dont give any parameters, '
            'if you want to get current month target of authenticated user, give "?method=userCurrentMonth" to url'
            '. If you want all target in currentMonth, give "?method=currentMonth"')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request):
        user = request.user
        name = request.data.get('name')
        target = Target(assigned_user=user, name=name, created_time=timezone.now())
        target.save()
        return Response(TargetSerializer(target, context={'request': request}).data)
    
    def update(self, request, pk):
        instance = Target.objects.get(id = pk)
        name = request.data.get('name')
        if name != "" and name != None:
            instance.__dict__.update({"name": name})
        point = int(request.data.get('point'))
        if point != "" and point != None:
            instance.__dict__.update({"point": Point.objects.get(id=point)})
        status = int(request.data.get('status'))
        if status != "" and status != None:
            instance.__dict__.update({"status": status})
        instance.save()
        return Response(TargetSerializer(instance, context={'request': request}).data)
        


class BonusPointViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = BonusPointSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateBonusPointSerializer
        elif self.action == 'update':
            return UpdateBonusPointSerializer
        else:
            return BonusPointSerializer

    def get_queryset(self):
        request = self.request
        user = self.request.user
        params = dict(request.query_params)
        method = params.get('method')
        query_set = BonusPoint.objects.all()
        if method is not None:
            if method[0] == 'currentMonth':
                cur_month = datetime.today().replace(day=1)
                query_set = Target.objects.filter(created_time__gt=cur_month, assigned_user=user)
        return query_set

    @action(detail=False, methods=['get'])
    def current_month(self, request, pk=None):
        request = request
        user = request.user
        params = dict(request.query_params)
        method = params.get('method')
        query_set = BonusPoint.objects.all()
        if method is not None:
            if method[0] == 'currentMonth':
                cur_month = datetime.today().replace(day=1)
                query_set = Target.objects.filter(created_time__gt=cur_month, assigned_user=user)
        return Response(BonusPointSerializer(query_set, many=True).data)

    @swagger_auto_schema(responses={'200': openapi.Response('Response Description', BonusPointSerializer)})
    @parser_classes((MultiPartParser, JSONParser))
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)
        
    @swagger_auto_schema(responses={'200': openapi.Response('Response Description', BonusPointSerializer)})
    @parser_classes((MultiPartParser, JSONParser))
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

@swagger_auto_schema(
    method='POST',
    operation_description='Create a basic user',
    operation_id='Create User',
    responses={
        '200': openapi.Response('Response Description', CustomMemberSerializer),
    },
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ),
    query_serializer=CreateUserSerializer,
)
@api_view(['POST'])
@permission_classes((AllowAny,))
@parser_classes([MultiPartParser, JSONParser, ])
def create_user(request):
    print(request.method)
    if request.method == 'GET':
        return Response({
            'error': "method is not allowed",
        })
    # print(request.data['username'])
    # return Response({"status": "Accepted Request"})
    username = request.data.get('username')
    password = request.data.get('password')
    check_queryset = CustomMember.objects.filter(username=username)
    print(check_queryset)
    if len(check_queryset) > 0:
        return Response({
            "error": "username has already existed"
        })
    new_mem = CustomMember(username=username)
    new_mem.set_password(password)
    new_mem.save()

    # add new user to General

    try:
        general_group = GroupPro.objects.get(name='General')
        general_group.members.add(new_mem)
        general_group.save()
    except:
        print('error')
    return Response(CustomMemberSerializer(new_mem, context={'request': request}).data)


# self define swagger field
@swagger_auto_schema(
    method='POST',
    operation_description='Create a post, post has 2 type',
    operation_id='Create a post',
    manual_parameters=[
        openapi.Parameter(
            name='files',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=False,
            description="Images that's pinned to Post",
        ),
        openapi.Parameter(
            name='content',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            requried=True,
            description="Content of the post",
        ),
        openapi.Parameter(
            name='group_id',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_NUMBER,
            required=True,
            description="Id of group that the post belong to",
        ),
        openapi.Parameter(
            name='polls',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_OBJECT,
            required=False,
            description="A list of Poll content you want to post"
        ),
        openapi.Parameter(
            name='type',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_INTEGER,
            required=True,
            description="Type of Post: '0' is normal post, '1' is polls with post",
        )
    ],
    responses={
        '200': openapi.Response('Response Description', PostSerializer),
    }
)
@api_view(['POST'])
@permission_classes((AllowAny,))
@parser_classes([MultiPartParser, ])
def create_post(request):
    # print(request.method)
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
    count_ = 0
    for count, x in enumerate(request.FILES.getlist("files")):

        def process(f):
            image = Image(img_url=f)
            image.save()
            new_post.photos.add(image)
        count_ = count
        process(x)
    # print(count)

    new_post.save()

    new_notification = Notification(
        assigned_post=new_post,
        assigned_user=request.user,
        type=0
    )
    new_notification.save()
    user_list = new_post.assigned_group.members
    
    relation_device_id_list = []
    for user in user_list.all():
        print('{} == {}'.format(user.id, request.user.id))
        if user.id == request.user.id:
            continue
        new_notification_member = NotificationMember(assigned_user=user, assigned_notification=new_notification)
        new_notification_member.save()
        user_device_list = UserDevice.objects.filter(assigned_user=user)
        for user_device in user_device_list:
            relation_device_id_list.append(user_device.device_id)
    
    send_to_onesignal_worker(APP_ID, relation_device_id_list, 'Đây là notification từ post {}'.format(new_post.id))
    
    return PostSerializer(new_post, context={'request': request}).data

@swagger_auto_schema(
    method='GET',
    operation_description='"?method=allTime" if you want to get all time rank, "?method=currentMonth" if you want to get current month rank'
)
@api_view(['GET'])
@permission_classes((AllowAny, ))
@renderer_classes([CamelCaseJSONRenderer])
def get_rank(request):
    method = request.GET.get('method')
    result_pair = []
    users = CustomMember.objects.filter()
    if method == "allTime":
        for user in users:
            score = 0
            # Get point from target
            targets = Target.objects.filter(assigned_user=user, is_done=True)
            for target in targets:
                score += target.point.score
            
            # get point from bonus point
            bonus_points = BonusPoint.objects.filter(assigned_user=user)
            for bonus_point in bonus_points:
                score += bonus_point.score
            
            user_data = AssignedUserSummary(user).data
            result_pair.append({
                "user": user_data,
                "score": score,
            })
            print(type(user_data))
    elif method == "currentMonth":
        for user in users:
            score = 0
            cur_month = datetime.today().replace(day=1)
            targets = Target.objects.filter(assigned_user=user, is_done=True, created_time__gt=cur_month)
            for target in targets:
                score += target.point.score

            bonus_points = BonusPoint.objects.filter(assigned_user=user, created_time__gt=cur_month)
            for bonus_point in bonus_points:
                score += bonus_point.score

            user_data = AssignedUserSummary(user)
            print(type(user_data))
            result_pair.append({
                "user": user_data,
                "score": score,
            })
    def take_score(obj):
        return obj.get('score')
    list.sort(result_pair, key=take_score, reverse=True)
    return Response(result_pair)
    
        
    
