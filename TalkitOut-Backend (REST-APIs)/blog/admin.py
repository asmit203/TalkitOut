from .models import post, announcements, Friend, Group
from django.contrib import admin

# Register your models here.
admin.site.register(post)
admin.site.register(announcements)
admin.site.register(Friend)
admin.site.register(Group)