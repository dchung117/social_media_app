from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"), # home page view
    path("signup", views.signup, name="signup") # user sign-up page view
]