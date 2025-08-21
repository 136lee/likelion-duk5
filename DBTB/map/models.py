from django.db import models

# Create your models here.

class Place(models.Model):
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=200)
    lat=models.FloatField()
    long=models.FloatField()
    dong = models.CharField(max_length=40, null=True, blank=True, db_index=True)

    def __str__(self):
        return f"{self.name} ({self.address})"
