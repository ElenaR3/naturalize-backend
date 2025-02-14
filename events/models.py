from django.db import models
from shared.models import Competences, Location, Team, Achievements

class Event(models.Model):
    event_types = [
        (1, 'VO'),
        (2, 'SE'),
    ]
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    startDate = models.DateTimeField(null=True, blank=True)
    endDate = models.DateTimeField(null=True, blank=True)
    eventName = models.TextField()
    markerType = models.IntegerField(choices=event_types) # event or VO
    eventDescription = models.TextField() 
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='event_locations')
    competences = models.ManyToManyField(Competences, related_name="event_comp") # This might get deleted
    achievements = models.ManyToManyField(Achievements, related_name="event_achv")
    focus_teams = models.ManyToManyField(Team, related_name='event_teams_focus')
    people_needed = models.PositiveIntegerField(default=0)
    people_applied = models.PositiveIntegerField(default=0)
    main_image_url = models.URLField(null=True, blank=True)
    event_xp = models.IntegerField(null=True, blank=True)
    organized_by = models.ForeignKey('ngo.NGOEntity', related_name="event_organizer", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['-updated']