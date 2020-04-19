from django.contrib import admin
from .models import Post, GroupPro, Comment, CustomMember, Reaction, Poll, Tick, Image

admin.site.register(CustomMember)
admin.site.register(Post)
admin.site.register(GroupPro)
admin.site.register(Comment)
admin.site.register(Reaction)
admin.site.register(Poll)
admin.site.register(Tick)
admin.site.register(Image)
