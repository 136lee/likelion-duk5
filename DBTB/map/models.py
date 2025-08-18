from django.db import models

# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=200, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name or f"{self.lat},{self.lng}"