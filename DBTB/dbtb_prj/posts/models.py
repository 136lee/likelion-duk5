from django.db import models
from users.models import User
import os
from uuid import uuid4
from django.utils import timezone

def upload_filepath(instance, filename):
    today_str = timezone.now().strftime("Y%m%d")
    file_basename = os.path.basename(filename)
    return f'{instance._meta.model_name}/{today_str}/{str(uuid4())}_{file_basename}'

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="posts")
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(to=Category, through='PostCategory')
    like = models.ManyToManyField(to=User, through='Like', related_name='like_posts')
    scrap = models.ManyToManyField(to=User, through='Scrap', related_name='scrap_posts')
    image = models.ImageField(upload_to=upload_filepath, blank=True)
    video = models.FileField(upload_to=upload_filepath, blank=True)


class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

class PostCategory(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)

class Like(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE,related_name='post_likes')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,related_name='user_likes')

class Scrap(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='post_scrap')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_scrap')