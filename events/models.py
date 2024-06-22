from distutils.text_file import TextFile
from django.db import models
from ngo.models import NGOEntity
#from ngo.models import NGOEntity
from shared.models import Competences, Location, Team

class Achievements(models.Model):
    name = models.TextField()
    description = models.TextField()
    xpGiven = models.IntegerField()

class Event(models.Model):
    event_types = [
        (1, 'VO'),
        (2, 'SE'),
    ]
    #id = models.IntegerField(primary_key=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) # take a snapshot only when created
    startDate = models.DateTimeField(null=True, blank=True)
    endDate = models.DateTimeField(null=True, blank=True)
    eventName = models.TextField()
    markerType = models.IntegerField(choices=event_types) # event or VO
    eventDescription = models.TextField() 
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='event_locations')
    competences = models.ManyToManyField(Competences, related_name="event_comp")
    achievements = models.ManyToManyField(Achievements, related_name="event_achv")
    team = models.ManyToManyField(Team, related_name='event_teams_focus')
    people_needed = models.PositiveIntegerField(default=0)
    people_applied = models.PositiveIntegerField(default=0)
    image_url = models.URLField(null=True, blank=True)
    event_xp = models.IntegerField(null=True, blank=True)
    organized_by = models.ForeignKey(NGOEntity, related_name="event_organizer", on_delete=models.CASCADE, blank=True, null=True)
    # todo: add Benefit

    class Meta:
        ordering = ['-updated']

class Photo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='gallery_photos')
    image = models.URLField()
    caption = models.CharField(max_length=255, blank=True)

# {
# "eventName": "TestName",
# "markerType": "event" ,
# "eventDescription": "descriptiontest",
# "location": {"latitude": "22.334", "longitude": "34.344"},
# "team": "marines"
# }