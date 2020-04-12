from django.contrib.auth.models import User
from django.db import models
from .enums import PostType


class Member(models.Model):
    assigned_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False, default=None
    )
    class_name = models.CharField(max_length=15, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=50, null=True, blank=True)
    role = models.SmallIntegerField()
    date_of_birth = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)


class GroupPro(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=1024, null=True, blank=True)


class Post(models.Model):
    userId = models.ForeignKey(
        Member, on_delete=models.CASCADE, default=None, null=False
    )
    groupId = models.ForeignKey(
        GroupPro, on_delete=models.CASCADE, null=True, default=None
    )
    content = models.CharField(max_length=3000)
    time = models.DateTimeField()
    type = models.SmallIntegerField(
        null=False,
        blank=False,
        default=PostType.NORMAL.value,
        choices=[
            (PostType.NORMAL.value, PostType.NORMAL.name),
            (PostType.TICK_POLL.value, PostType.TICK_POLL.name),
        ],
    )


class Comment(models.Model):
    userId = models.ForeignKey(
        Member, on_delete=models.CASCADE, null=False, default=None
    )
    postId = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, default=None)
    content = models.CharField(max_length=2048)
