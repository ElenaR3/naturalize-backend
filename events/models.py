from distutils.text_file import TextFile
from turtle import update
from django.db import models

# Create your models here.

class Event(models.Model):
    #id = models.IntegerField(primary_key=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) # take a snapshot only when created
    markerName = models.TextField()
    markerType = models.TextField()
    markerDescription = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    team = models.TextField()

    class Meta:
        ordering = ['-updated']