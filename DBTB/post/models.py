from django.db import models
from users.models import User
from map.models import *
import os
from uuid import uuid4
from django.utils import timezone


def upload_filepath(instance, filename):
    today_str=timezone.now().strftime("%Y%m%d")
    file_basename=os.path.basename(filename)
    return f'{instance._meta.model_name}/{today_str}/{str(uuid4())}_{file_basename}'

class Post(models.Model):
    content=models.TextField()
    image=models.ImageField(upload_to=upload_filepath, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    AI_matching=models.TextField(blank=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    place=models.ManyToManyField(Place, related_name="post_place")
    scrap = models.ManyToManyField(User, related_name="scrapped_posts", blank=True, through="PostScrap")
    video = models.FileField(upload_to=upload_filepath, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)


    def __str__(self):
        return f'{self.id})[{self.author}]-{self.content[:15]}...'
    
class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    
class AIFeedback(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="ai_post")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ai_user")
    is_positive = models.BooleanField()  # True=만족, False=불만족

    def __str__(self):
        return f'[{self.post.pk}]{self.post.AI_matching[:15]} - {self.is_positive}'
    

class Recommend(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_recom")
    recom_now = models.TextField(blank=True)
    recom_later = models.TextField(blank=True, default="")
    comment=models.TextField(blank=True)

    def __str__(self):
        base = self.recom_now or self.recom_later or ""
        return f'{self.post.pk} - {base[:20]}'
    
class PostCategory(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="post_categories")
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name="post_categories")


class PostScrap(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # 언제 스크랩했는지 기록

    class Meta:
        unique_together = ('post', 'user')  # 중복 스크랩 방지

    def __str__(self):
        return f"{self.user.username} scrapped {self.post.id}"