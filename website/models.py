from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

class User(AbstractUser):
    pass

class Member(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="user")
    name = models.CharField(max_length=30)
    admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} is an admin: {self.admin}"