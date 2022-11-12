from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

class User(AbstractUser):
    pass