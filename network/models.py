from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="profile_user")
    following = models.ManyToManyField('User', default=None, blank=True, null=True, related_name="following")
    followers = models.ManyToManyField('User', default=None, blank=True, null=True, related_name="followers")
    
    def __str__(self):
        return f"{self.user} has {self.followers} followers and {self.following} followings"

class Comment(models.Model):
    comment_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="user_comments")
    commentInput = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.comment_user}: {self.commentInput}"
        
class Like(models.Model):
    like_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="user_like")
    like_post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="user_like")

class Post(models.Model):
    content = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name="post_profile")
    liked = models.ManyToManyField('User', default=None, blank=True, related_name='post_likes')
    comment = models.ManyToManyField('Comment', related_name="post_comments", blank=True)

    def __str__(self):
        return f"{self.owner} posted {self.content}"

