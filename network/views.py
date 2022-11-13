from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator
from django.utils import timezone

from .models import *

from nrclex import NRCLex
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import random
from datetime import datetime
import string
from PIL import Image, ImageDraw

def drawgraph(result):
    emotions = {
        'fear': [[172,154,186], [120,100,152], [123,63,165], [101,70,122], [72,62,84]], 
        'anger': [[231,34,34], [201,41,41], [184,47,47], [171,50,50], [150,50,50]], 
        'anticipation': [[241, 222, 193], [205, 182, 153], [105, 135, 121], [214, 200, 158], [252, 243, 197]], 
        'trust': [[253,147,174], [111,225,225], [246,197,99], [223,150,75], [164,75,0]], 
        'surprise': [[255, 255, 255], [255, 248, 232], [252, 213, 129], [213, 41, 65], [153, 13, 53]], 
        'positive': [[253, 253, 189], [200, 255, 212], [184, 232, 252], [77, 175, 255], [240, 255, 66]], 
        'negative': [[101,151,197], [147,191,69], [152,130,37], [139,66,25], [45,11,0]], 
        'sadness': [[36,36,36], [84,68,68], [118,118,97], [129,146,121], [193,190,132]], 
        'disgust': [[225,145,24], [195,120,43], [141,92,17], [212,131,29], [229,155,14]], 
        'joy': [[230,27,27], [247,244,241], [243,229,10], [10,113,243], [199,34,224]]
    }

    highestEmotion = max(result, key=result.get)

    colors = emotions[highestEmotion]

    print(colors)
        
    figure = ''.join(random.choices(string.ascii_lowercase, k=32))

    image = Image.new('RGB', (2000, 2000))
    width, height = image.size

    rectangle_width = 100
    rectangle_height = 100

    number_of_squares = 10000

    draw_image = ImageDraw.Draw(image)

    for i in range(number_of_squares):
        rectangle_x = random.randint(0, width)
        rectangle_y = random.randint(0, height)

        rectangle_shape = [
            (rectangle_x, rectangle_y),
            (rectangle_x + rectangle_width, rectangle_y + rectangle_height)]

        j = random.randint(0, 4)
        draw_image.rectangle(
            rectangle_shape,
            fill=(
                colors[j][0],
                colors[j][1],
                colors[j][2]
            )
        )

    # plt.savefig("static/images/" + figure + ".png")
    image.save("static/images/" + figure + ".png")

    return (figure + ".png")

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
        if Post.objects.filter(owner=user).exists():
            all_posts = Post.objects.filter(owner=user).order_by('-time')
            if (all_posts.first().time == timezone.now):
                status = True
            else:
                status = False
            
            # Render posts in order of 10 per paginator
            paginator = Paginator(all_posts, 10)
            page_number = request.GET.get('page')
            posts = paginator.get_page(page_number)
            return render(request, "network/index.html", {
                "form": CreatePost(),
                'posts': posts,
                'status': status
            })
        else:
            return render(request, "network/index.html", {
                "form": CreatePost(),
                'status': True
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
        sentiment = 100
        post = Post(
            content = description,
            owner = User.objects.get(username=request.user),
            sentiment = sentiment,
            image = drawgraph(getemotions(description))
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

def calendar(request):
    user = request.user
    all_posts = Post.objects.filter(owner=user).order_by('time')
    return render(request, "network/calendar.html",{
        "posts": all_posts
    })

def resources(request):
    return render(request, "network/healthresources.html")