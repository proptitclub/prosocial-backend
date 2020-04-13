from django.contrib import admin
from .models import Post, GroupPro, Comment, Member, Reaction, Poll, Tick

admin.site.register(Member)
admin.site.register(Post)
admin.site.register(GroupPro)
admin.site.register(Comment)
admin.site.register(Reaction)
admin.site.register(Poll)
admin.site.register(Tick)
