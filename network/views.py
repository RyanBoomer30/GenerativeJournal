from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator

from .models import *

class CreatePost(forms.Form):
    content = forms.CharField(
        label="", 
        max_length=120, 
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'What is happening?'}))

def index(request):
    user = request.user
    all_posts = Post.objects.all()

    # Render posts in order of 10 per paginator
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "form": CreatePost(),
        'posts': posts
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        newprofile = Profile.objects.create(user=user)
        newprofile.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# Create a new post
def createPost(request):
    if request.method == "POST":
        description = request.POST['content']
        post = Post(
            content = description,
            owner = User.objects.get(username=request.user),
        )
        post.save()
        return HttpResponseRedirect(reverse("index"))

# Render profile
def profile(request, profile_id):
    profile = Profile.objects.get(user=profile_id)
    userpost = Post.objects.filter(owner=profile_id)
    paginator = Paginator(userpost, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html",{
        "posts" : page_obj,
        "profile": profile,
        "userName": profile.user.username,
        "id": profile_id,
    })
    
# Edit the content of post_id
def edit(request, post_id, edit):
    edited_post = Post.objects.get(id=post_id)
    edited_post.content = edit
    edited_post.save()
    return JsonResponse({
        'edit': edit
    })

    