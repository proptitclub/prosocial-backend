from django.contrib import admin
from .models import Post, GroupPro, Comment, CustomMember, Reaction, Poll, Tick, Image, Notification, NotificationMember, UserDevice

admin.site.register(CustomMember)
admin.site.register(Post)
admin.site.register(GroupPro)
admin.site.register(Comment)
admin.site.register(Reaction)
admin.site.register(Poll)
admin.site.register(Tick)
admin.site.register(Image)
admin.site.register(Notification)
admin.site.register(NotificationMember)
admin.site.register(UserDevice)
