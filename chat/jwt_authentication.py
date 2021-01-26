from channels.auth import AuthMiddlewareStack
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.backends import TokenBackend
from django.contrib.auth.models import AnonymousUser
from prosocial.models import CustomMember
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user(valid_data):
    return CustomMember.objects.get(id=valid_data['user_id'])

class TokenAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)
    

class TokenAuthMiddlewareInstance:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, send, receive):
        headers = dict(self.scope['headers'])
        print("Headers", headers)
        if b'sec-websocket-protocol' in headers:

            try:
                token_name, token_key = headers[b'sec-websocket-protocol'].decode().split('%space%')
                if token_name == 'Bearer':
                    valid_data = TokenBackend(algorithm='HS256').decode(token_key, verify=False)
                    print(valid_data['user_id'])
                    # print("Access_token", access_token)
                    # user = CustomMember.objects.get(id=valid_data['user_id'])
                    user = await get_user(valid_data)
                    print("Token key: ", token_key)
                    self.scope['user'] = user
                    print(user)
                    print("Embedded user to header")
            except TokenError:
                self.scope['user'] = AnonymousUser()
        inner = self.inner(self.scope)
        return await inner(receive, send)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))