from datetime import datetime as dt
import uuid
from django.db import models
from django.contrib.auth import get_user_model

# Get base user model
USER = get_user_model()

# Create your models here.
class Profile(models.Model): # User profile
    user = models.ForeignKey(USER, on_delete=models.CASCADE) # foreign key to USER model, delete foreign keys in EVERY LINKED model
    id_user = models.IntegerField()
    bio = models.TextField(blank=True) # blank -> optional text field
    profile_img = models.ImageField(upload_to="profile_imgs", default="blank-profile-picture.png") # provide default profile pic (if not given)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model): # User post
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100) # user who posted
    image = models.ImageField(upload_to="post_imgs")
    caption = models.TextField()
    created_at = models.DateTimeField(default=dt.now)
    num_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class LikePost(models.Model): # Liked user post
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Followers(models.Model): # followers for a user
    user = models.CharField(max_length=100)
    follower = models.CharField(max_length=100)

    def __str__(self):
        return self.user