from django.db import models
from users.models import User
import os
from uuid import uuid4
from django.utils import timezone

def upload_filepath(instance, filename):
    today_str = timezone.now().strftime("Y%m%d")
    file_basename = os.path.basename(filename)
    return f'{instance._meta.model_name}/{today_str}/{str(uuid4())}_{file_basename}'

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="posts")
    category = models.ManyToManyField(to=Category, through="PostCategory", related_name="posts")
    image = models.ImageField(upload_to=upload_filepath, blank=True)
    video = models.FileField(upload_to=upload_filepath, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

# class Post(models.Model):
   # AI_matching=models.TextField()
   # author=models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    #place=models.ForeignKey(Place, on_delete=models.CASCADE, related_name="post_place")
   # scrab=models.ManyToManyField(User, related_name="post_scrab")

  #  def __str__(self):
    #    return f'[{self.author}]-{self.content[:15]}...'
    def __str__(self):
        return f'[{self.id}] {self.title}'
    
class PostCategory(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="post_categories")
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name="post_categories")