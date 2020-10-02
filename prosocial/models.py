from django.contrib.auth.models import User, AbstractUser
from django.db import models
from .enums import *
from django.conf import settings
import uuid


def custom_media_path(instance, filename):
    file_ext = filename.split(".")[-1]
    return str(uuid.uuid4()) + "." + file_ext


class Image(models.Model):
    img_url = models.FileField(
        upload_to=custom_media_path, max_length=100, default="default.jpg"
    )


class CustomMember(AbstractUser):
    avatar = models.FileField(
        upload_to=custom_media_path, max_length=100, default="default.jpg"
    )
    user_gender = models.SmallIntegerField(
        null=False,
        blank=False,
        default=GenderType.MALE.value,
        choices=[
            (GenderType.MALE.value, GenderType.MALE.name),
            (GenderType.FEMALE.value, GenderType.FEMALE.name),
            (GenderType.OTHER.value, GenderType.OTHER.name),
        ],
    )
    cover = models.FileField(
        upload_to=custom_media_path, max_length=100, default="default.jpg"
    )
    # avatar = models.ForeignKey(Image, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=15, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=50, null=True, blank=True)
    role = models.SmallIntegerField(null=True, blank=True, default=0)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return "custom_user: {}".format(self.username)


class GroupPro(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=1024, null=True, blank=True)
    admins = models.ManyToManyField(CustomMember, related_name="admins")
    members = models.ManyToManyField(
        CustomMember, related_name="members", null=True, blank=True, default=None
    )
    cover = models.FileField(
        upload_to=custom_media_path, max_length=100, default="default.jpg"
    )
    def __str__(self):
        return self.name


class Post(models.Model):
    assigned_user = models.ForeignKey(
        CustomMember, on_delete=models.CASCADE, default=None, null=False
    )
    assigned_group = models.ForeignKey(
        GroupPro, on_delete=models.CASCADE, null=True, default=None
    )
    content = models.CharField(max_length=3000)
    time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    photos = models.ManyToManyField(
        Image, related_name="images", null=True, blank=True, default=None
    )
    type = models.SmallIntegerField(
        null=False,
        blank=False,
        default=PostType.NORMAL.value,
        choices=[
            (PostType.NORMAL.value, PostType.NORMAL.name),
            (PostType.TICK_POLL.value, PostType.TICK_POLL.name),
        ],
    )

    def __str__(self):
        return "{} - {} - {}".format(
            self.assigned_user.username, self.content, self.assigned_group.name
        )


class Comment(models.Model):
    assigned_user = models.ForeignKey(
        CustomMember, on_delete=models.CASCADE, null=False, default=None
    )
    assigned_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=False, default=None
    )
    content = models.CharField(max_length=2048)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.assigned_user.username + " - " + self.content


class Reaction(models.Model):
    assigned_user = models.ForeignKey(
        CustomMember, on_delete=models.CASCADE, null=False, default=None
    )
    assigned_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=False, default=None
    )
    type = models.SmallIntegerField(
        null=True,
        blank=True,
        choices=[
            (ReactionType.LIKE.value, ReactionType.LIKE.name),
            (ReactionType.HEART.value, ReactionType.HEART.name),
            (ReactionType.HAHA.value, ReactionType.HAHA.name),
            (ReactionType.WOW.value, ReactionType.WOW.name),
            (ReactionType.ANGRY.value, ReactionType.ANGRY.name),
        ],
    )

    def __str__(self):
        return self.assigned_user.username + " - " + ReactionType.get_name(self.type)


class Poll(models.Model):
    assigned_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=False, default=None
    )
    question = models.CharField(max_length=1024)

    def __str__(self):
        return self.question + " - " + self.assigned_post.content


class Tick(models.Model):
    assigned_poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, null=False, default=None
    )
    assigned_user = models.ForeignKey(CustomMember, null=True, blank=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.assigned_poll.question


class UserDevice(models.Model):
    assigned_user = models.ForeignKey(
        CustomMember, on_delete=models.CASCADE, null=False, default=None
    )
    device_id = models.CharField(max_length=128)

    def __str__(self):
        return self.assigned_user.display_name

class Notification(models.Model):
    assigned_user = models.ForeignKey(
        CustomMember, on_delete=models.CASCADE, null=False, default=None
    )
    
    assigned_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=False, default=None
    )

    type = models.SmallIntegerField(
        null=False,
        blank=False,
        default=NotificationType.INIT.value,
        choices=[
            (NotificationType.INIT.value, NotificationType.INIT.name),
            (NotificationType.LIKE.value, NotificationType.LIKE.name),
            (NotificationType.COMMENT.value, NotificationType.COMMENT.name)
        ],
    )

    created_time = models.DateTimeField(auto_now_add=True)


    # def __str__(self):
    #     return self.assigned_user.first_name + ' ' + self.assigned_user.last_name + '/' + self.assigned_post.id


class NotificationMember(models.Model):
    assigned_user = models.ForeignKey(
        CustomMember, on_delete=models.CASCADE, null=False, default=None
    )

    assigned_notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, null=False, default=None
    )

    is_seen = models.BooleanField(null=False, default=False)

    # def __str__(self):
    #     return self.assigned_user.first_name + ' ' + self.assigned_user.last_name + '/' + self.notification.assigned_post.id



class Point(models.Model):
    score = models.IntegerField(default=0)
    description = models.CharField(max_length=256)

class Target(models.Model):
    assigned_user = models.ForeignKey(
        CustomMember, null=False, default=None, on_delete=models.CASCADE
    )

    name = models.CharField(max_length=256, default="")
    is_done = models.BooleanField(default=False)
    point = models.ForeignKey(
        Point, null=False, default=None, on_delete=models.CASCADE
    )

    status = models.SmallIntegerField(
        null=False,
        blank=False,
        default=TargetStatusType.NOT_SCORED.value,
        choices=[
            (TargetStatusType.NOT_SCORED.value, TargetStatusType.NOT_SCORED.name),
            (TargetStatusType.SCORED.value, TargetStatusType.SCORED.name),
            (TargetStatusType.CONFIRM.value, TargetStatusType.CONFIRM.name)
        ],
    )

    created_time = models.DateTimeField()

class BonusPoint(models.Model):
    assigned_user = models.ForeignKey(
        CustomMember, null=False, default=None, on_delete=models.CASCADE
    )
    score = models.IntegerField(default=0)
    description = models.CharField(max_length=256)
    created_time = models.DateTimeField(auto_now_add=True)
