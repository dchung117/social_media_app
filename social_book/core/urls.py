from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"), # home page view
    path("signup", views.signup, name="signup"), # user sign-up page view
    path("signin", views.signin, name="signin"), # user sign-in page view
    path("logout", views.logout, name="logout"), # user logout
    path("settings", views.settings, name="settings"), # account settings
    path("upload", views.upload, name="upload"), # uploading posts
    path("like-post", views.like_post, name="like_post"), # liking post
    path("profile/<str:pk>", views.profile, name="profile"), # profile page
    path("follow", views.follow, name="follow"), # follow user
    path("search", views.search, name="search") # search for user
]