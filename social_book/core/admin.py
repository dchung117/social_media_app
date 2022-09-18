from django.contrib import admin
from .models import Profile, Post, LikePost

# Register your models here.
admin.site.register(Profile) # register the profile/post models so admins can view them
admin.site.register(Post)
admin.site.register(LikePost)