from django.db import models
from .constants import TeamChoices

class Competences(models.Model):
    name = models.TextField()
    description = models.TextField()

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    text = models.TextField()

class Team(models.Model):
    name = models.IntegerField(
        choices=TeamChoices.choices,
    )

    def __str__(self):
        return self.get_name_display()

class PhotoBase(models.Model):
    image = models.URLField()
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True 
    
    def __str__(self):
        return self.caption or 'No caption'
    
class Photo(PhotoBase):
    pass