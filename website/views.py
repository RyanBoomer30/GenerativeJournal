from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django import forms
from django.views.generic import CreateView
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
import json

from .models import *

def index(request):
    return HttpResponse("website")