from distutils.text_file import TextFile
from sqlite3 import DataError
from django.db import models

from user.models import CustomUser

# Create your models here.

class Event(models.Model):
    #id = models.IntegerField(primary_key=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) # take a snapshot only when created
    startDate = models.DateTimeField(null=True, blank=True)
    endDate = models.DateTimeField(null=True, blank=True)
    eventName = models.TextField()
    markerType = models.TextField() # event or VO
    eventDescription = models.TextField() 
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True, related_name='event_locations')
    competences = models.ManyToManyField('Competences', related_name="event_comp")
    achievements = models.ManyToManyField('Achievements', related_name="event_achv")
    savedByUser = models.ManyToManyField(CustomUser, related_name="event_saved_by_user")
    createdByUser = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='event_CreatedBy')
    team = models.TextField()
    image_url = models.URLField(null=True, blank=True)
    image_file = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if self.image_url is None and self.image_file is None:
            raise DataError("Image_url and image_file cannot both be null")
        super().save(*args, **kwargs)

    @property
    def image(self) -> str:
        if self.image_file is not None:
            return self.image_file.url
        else:
            return self.image_url

    class Meta:
        ordering = ['-updated']

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    text = models.TextField()

class Competences(models.Model):
    name = models.TextField()
    description = models.TextField()

class Achievements(models.Model):
    name = models.TextField()
    description = models.TextField()
    xpGiven = models.IntegerField()


# {
# "eventName": "TestName",
# "markerType": "event" ,
# "eventDescription": "descriptiontest",
# "location": {"latitude": "22.334", "longitude": "34.344"},
# "team": "marines"
# }