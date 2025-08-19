from django.db import models

# Create your models here.

class Place(models.Model):
    place_name=models.CharField(max_length=50)
    address=models.CharField(max_length=200)
    latitude=models.FloatField()
    longtitude=models.FloatField()

    def __str__(self):
        return f"{self.place_name} ({self.address})"
