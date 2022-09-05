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