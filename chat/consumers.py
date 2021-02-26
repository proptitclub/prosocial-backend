# chat/consumers.py
import json
from .models import *
from prosocial.models import *
import socketio
import functools
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.backends import TokenBackend
from django.contrib.auth.models import AnonymousUser
import redis
from .enums import *

red = redis.Redis(host='localhost', port=6379, db=0)

sio = socketio.Server(
    async_mode='gevent_uwsgi',
    cors_allowed_origins=["http://localhost:3000", "http://proptit.social/*", "http://localhost:9090"],
    logger=True,
    engineio_logger=True,
)

def auth_deco(f):
    def wrapper(sid=None, environ=None):
        sid_user_id = red.get('socketio---{}'.format(sid)).decode('utf-8')
        req_user_id = environ.get('user').get('id')
        room_id = environ.get('roomID')
        print('sid_token: {}'.format(sid_user_id))
        print('req_token: {}'.format(req_user_id))
        if sid_user_id != req_user_id:
            environ['valid'] = False
            value = red.get('socketio-room---{}-{}'.format(req_user_id, room_id))
            if value is not None:
                environ['user_room_id'] = value
                environ['valid'] = True
            else:
                environ['valid'] = False
        else:
            environ['valid'] = True

        f(sid, environ)
    
    return wrapper


@sio.on('newMessage', namespace='/')
@auth_deco
def new_message(sid=None, environ=None):
    print(environ.get('valid'))
    if environ.get('valid') == True:
        sio.emit(
            'newMessage', 
            {
                'data': environ.get('data'), 
                'user': 
                {
                    'id': environ.get('user').get('id'),
                    'avatar': environ.get('user').get('avatar'),
                    'display_name': environ.get('user').get('display_name'),
                }, 
                'id':sid
            }, 
            room=environ.get('roomID')
        )
        user_room = UserRoom.objects.get(id=int(environ.get('user_room_id')))
        new_message = Message(
            user_room=user_room,
            content=environ.get('data'),
            type=MessageType.TEXT.value,
        )
        new_message.save()
    else:
        sio.emit('newMessage', {'status': 'fail', 'id':sid}, room=sid)
        sio.disconnect(sid)

@sio.on('connect', namespace='/')
def test_connect(sid=None, environ=None):
    print(environ)
    try:
        auth_token = None
        for key in environ:
            if key == 'HTTP_AUTHORIZATION':
                auth_token = environ[key]
            # print("{} - {}".format(key, environ[key]))
        # auth_token = environ.get('HTTP_AUTHORIZATION')
        if auth_token is None:
            print("NO TOKEN IN HEADER")
        token_name, token_key = auth_token.split(' ')
        if token_name == 'Bearer':
            valid_data = TokenBackend(algorithm='HS256').decode(token_key, verify=False)
    except Exception as e:
        print("Error when authorization")
        sio.emit('disconnect', {'status': -1, 'msg': "Something wrong | invalid token or no token provided"})
        sio.disconnect(sid)
        return

    user_id = valid_data.get('user_id')
    user = CustomMember.objects.get(id=user_id)
    room_id = int(environ.get('HTTP_ROOMID'))
    room = Room.objects.get(id=room_id)
    user_room = UserRoom.objects.filter(room=room, user=user)
    if len(user_room) > 0:
        # we just need to set socketio-room---user-room is exist or not
        # so value can be anything, and be fixed
        red.set('socketio-room---{}-{}'.format(user_id, room_id), user_room[0].id)
    else:
        print("Error when authorization")
        sio.emit('disconnect', {'status': -1, 'msg': "Something wrong | invalid token or no token provided"})
        sio.disconnect(sid)
        return
    sio.enter_room(sid, room.id)
    red.set('socketio---{}'.format(sid), valid_data.get('user_id'))
    sio.emit(
        'connect', 
        {
            'data': 'Connected', 
            'count': 0, 
            'user': {
                "id": valid_data.get('user_id'),
                "avatar": 'http://' + environ.get('HTTP_HOST') + '/' + user.avatar.url,
                "display_name": user.display_name,
            }
        },
        namespace='/'
    )

@sio.on('leave room', namespace='/')
@auth_deco
def leave_room(sid, environ):
    sio.leave_room(sid, int(environ.get('roomID')))

@sio.on('disconnect', namespace='/')
def disconnect(sid):
    print('Client disconnected')
