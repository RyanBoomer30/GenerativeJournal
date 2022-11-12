from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="profile_user")
    
    def __str__(self):
        return f"{self.user} has {self.followers} followers and {self.following} followings"
        
class Post(models.Model):
    content = models.CharField(max_length=1000)
    time = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name="post_profile")
    sentiment = models.IntegerField()
    image = models.ImageField(default='default.png')

    def __str__(self):
        return f"{self.owner} posted {self.content}"

