from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class NewPost(models.Model):
    content = models.TextField(null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    likes = models.IntegerField(default=0)
    comment = models.CharField(max_length=200, blank=True)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    
    class Meta:
        unique_together = ('follower', 'following')

class Likes(models.Model):
    liked = models.BooleanField(default=False)
    liked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    liked_post = models.ForeignKey(NewPost, on_delete=models.CASCADE, related_name='liked_by')

    class Meta:
        unique_together = ('liked_user', 'liked_post')
