from django.contrib import admin
from .models import Post, GroupPro, Comment, Member

admin.site.register(Member)
admin.site.register(Post)
admin.site.register(GroupPro)
admin.site.register(Comment)
