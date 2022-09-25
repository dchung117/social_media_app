from itertools import chain

from pyexpat import model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from . import views, models

# Create your views here.
@login_required(login_url="signin")
def index(request: HttpRequest) -> HttpResponse:
    # Get user profile object
    user_profile = models.Profile.objects.get(user=request.user)

    # Get all users that logged in user is following
    user_followers = [f.user for f in models.Followers.objects.filter(follower=request.user.username)]

    # Get the user's post feed list
    posts = []
    for u in user_followers:
        u_posts = models.Post.objects.filter(user=u)
        posts.append(u_posts)
    post_feed = list(chain(*posts))
    return render(request, "index.html", context={"user_profile": user_profile, "post_feed": post_feed}) # remder home page w/ index.html

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

                # Log user in
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # Create profile model for user
                user_model = User.objects.get(username=username) # get the saved user model
                new_profile = models.Profile.objects.create(user=user_model, # create profile model using the saved user_model
                    id_user=user_model.id)
                new_profile.save()
                return redirect("settings") # redirect to settings page
        else:
            messages.info(request, "Passwords do not match.")
            return redirect("signup")
    else: # render signup page
        return render(request, "signup.html") # render sign-up page w/ signup.html

def signin(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # Get username and password
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate username
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Invalid username and/or password")
            return redirect("signin")
    return render(request, "signin.html")

@login_required(login_url="signin")
def logout(request: HttpRequest) -> HttpResponse:
    # Authenticate logout
    auth.logout(request)

    return redirect("signin")

@login_required(login_url="signin")
def settings(request: HttpRequest) -> HttpResponse:
    # Get user profile
    user_profile = models.Profile.objects.get(user=request.user)

    # Get bio and location
    if request.method == "POST":
        # Check if profile was updated
        if request.FILES.get("image") is None: # profile image
            image = user_profile.profile_img # default image
        else:
            image = request.FILES.get("image")

        bio = request.POST["bio"]
        location = request.POST["location"]

        user_profile.profile_img = image
        user_profile.bio = bio
        user_profile.location = location

        # Save the user profile
        user_profile.save()

        return redirect("settings")

    return render(request, "setting.html", context={"user_profile": user_profile})

@login_required(login_url="signin")
def upload(request: HttpRequest) -> HttpResponse:
    # Check for post was uploaded
    if request.method == "POST":
        # Get user who made post
        user = request.user.username
        image = request.FILES.get("upload_img")
        caption = request.POST.get("caption")

        # Check if user uploaded empty post
        if (image is None) or len(caption) == 0:
            messages.info(request, "Please upload an image and write a caption.")
            return redirect("/")

        # Create a new post
        user_post = models.Post.objects.create(user=user, image=image, caption=caption)
        user_post.save()

    return redirect("/")

@login_required(login_url="signin")
def like_post(request: HttpRequest) -> HttpResponse:
    # Get username
    username = request.user.username

    # Get post from post_id
    post_id = request.GET.get("post_id")
    post = models.Post.objects.get(id=post_id)

    # Check if user has liked this post
    like_filter = models.LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter is None:
        # Create like post
        like_post = models.LikePost.objects.create(post_id=post_id, username=username)

        # Update number of likes
        post.num_likes = post.num_likes + 1

        like_post.save()
        post.save()
    else:
        # Remove like post
        like_filter.delete()

        # Update number of likes
        post.num_likes = post.num_likes - 1
        post.save()

    return redirect("/")

@login_required(login_url="signin")
def profile(request: HttpRequest, pk: str) -> HttpResponse:
    # Get viewing user
    viewing_user = User.objects.get(username=request.user)

    # Get user profile object
    user_object = User.objects.get(username=pk)
    user_profile = models.Profile.objects.get(user=user_object)

    # Get user posts
    user_posts = models.Post.objects.filter(user=pk)
    num_user_posts = len(user_posts)

    # Get user followers
    user_followers = models.Followers.objects.filter(user=pk)
    num_user_followers = len(user_followers)

    # Get user following
    user_following = models.Followers.objects.filter(follower=pk)
    num_user_following = len(user_following)

    # Check if viewing user is following profile user
    if models.Followers.objects.filter(follower=viewing_user, user=pk).first():
        follow_button = "Unfollow"
    else:
        follow_button = "Follow"

    context = {
        "object": user_object,
        "profile": user_profile,
        "posts": user_posts,
        "num_posts": num_user_posts,
        "num_followers": num_user_followers,
        "num_following": num_user_following,
        "follow_button": follow_button
    }
    return render(request, "profile.html", context=context)

@login_required(login_url="signin")
def follow(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # Get follower and user names
        follower = request.POST["follower"]
        user = request.POST["user"]

        # Determine if follower is already following user
        user_follower = models.Followers.objects.filter(user=user, follower=follower).first()

        # Toggle follow/unfollow
        if user_follower is None: # add follower
            new_follower = models.Followers.objects.create(user=user, follower=follower)
            new_follower.save()
        else:
            user_follower = models.Followers.objects.get(user=user, follower=follower)
            user_follower.delete()
    return redirect(f"/profile/{user}")

@login_required(login_url="signin")
def search(request: HttpRequest) -> HttpResponse:
    # Get search user's profile
    user_object = User.objects.get(username=request.user)
    user_profile = models.Profile.objects.get(user=user_object)
    if request.method == "POST":
        # Get searched username
        search_username = request.POST["search_user"]

        # Get all profiles that match username
        search_users = User.objects.filter(username__icontains=search_username)

        search_profiles = []
        for su in search_users:
            su_profile = models.Profile.objects.filter(id_user=su.id)
            search_profiles.append(su_profile)
        search_profiles = list(chain(*search_profiles))

        # Display search results
        context = {"user":user_object,
            "user_profile": user_profile,
            "search_profiles": search_profiles
            }
        return render(request, "search.html", context=context)
