from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpRequest, HttpResponse

from . import views, models

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html") # remder home page w/ index.html

def signup(request: HttpRequest) -> HttpResponse:
    # Save sign-up information
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["password2"]

        # Check that passwords match
        if password == confirm_password:
            # Check if email (i.e. account) already exists
            if User.objects.filter(email=email).exists():
                messages.info(request, "An account with this email already exists.")
                return redirect("signup")
            # Check if username is already taken
            elif User.objects.filter(username=username).exists():
                messages.info(request, "An account with this username already exists.")
                return redirect("signup")
            # Create account, save to database
            else:
                # Create a new user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Log user in, redirect to settings page

                # Create profile model for user
                user_model = User.objects.get(username=username) # get the saved user model
                new_profile = models.Profile.objects.create(user=user_model, # create profile model using the saved user_model
                    id_user=user_model.id)
                new_profile.save()
                return redirect("signup")
        else:
            messages.info(request, "Passwords do not match.")
            return redirect("signup")
    else: # render signup page
        return render(request, "signup.html") # render sign-up page w/ signup.html