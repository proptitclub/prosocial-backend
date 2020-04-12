from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Member


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


class MemberSerializer(serializers.ModelSerializer):
    assigned_user = UserSerializer()

    class Meta:
        model = Member
        fields = ["assigned_user", "display_name"]
