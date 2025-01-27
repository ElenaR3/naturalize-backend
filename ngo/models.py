from django.db import models

from shared.models import Team

class NGOEntity(models.Model):
    name = models.TextField()
    about = models.TextField(null=True, blank=True)
    history = models.TextField(null=True, blank=True)
    profile_image_url = models.URLField(null=True, blank=True)
    volonteer_num = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    total_xp = models.IntegerField(default=0)
    ngo_profile_gallery = models.ManyToManyField('shared.Photo', related_name='ngo_gallery', blank=True)
    focus_teams = models.ManyToManyField(Team, related_name='ngo_focus_teams', null=True, blank=True)