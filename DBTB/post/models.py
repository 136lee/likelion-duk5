from django.db import models
from django.contrib.auth import get_user_model
from map.models import Place

User = get_user_model()

class Post(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="posts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)