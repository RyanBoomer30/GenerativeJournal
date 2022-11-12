from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator

from .models import *

from nrclex import NRCLex
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as plt

def drawgraph(result):
  emotions = {'fear': 'm', 'anger': 'r', 'anticipation': 'm', 'trust': 'g', 'surprise': 'y', 'positive': 'y', 'negative': 'r', 'sadness': 'b', 'disgust': 'g', 'joy': 'y'}
  x = []
  y = []
  colors = []

  for key in result:
    x += [key]
    y += [result[key]]
    colors += emotions[key]
    

  plt.bar(x,y, color=colors, alpha=0.65)

  plt.xticks([])
  plt.yticks([])

  return plt

def getemotions(str):
    text_object = NRCLex(str)
    data = text_object.raw_emotion_scores
    return data

class CreatePost(forms.Form):
    content = forms.CharField(
        label="", 
        max_length=120, 
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'It looks like you have not posted anything'}))

def index(request):
    user = request.user
    if (user.is_authenticated):
        all_posts = Post.objects.filter(owner=user).order_by('-time')

        # Render posts in order of 10 per paginator
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "form": CreatePost(),
            'posts': posts
        })
    else:
        return render(request, "network/login.html")

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
        description = request.POST.get('postContent', False)
        dict = getemotions(description)   
        sentiment = 100
        post = Post(
            content = description,
            owner = User.objects.get(username=request.user),
            sentiment = sentiment,
            image = dict.savefig('{}.png'.format(post.id))
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