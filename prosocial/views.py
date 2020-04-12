from django.contrib.auth.models import User
from rest_framework import viewsets

from .serializers import UserSerializer, MemberSerializer

from .models import Member


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
