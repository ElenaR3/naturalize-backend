from django.db import models
from shared.constants import SocialMedia, ContactType

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
    focus_teams = models.ManyToManyField('shared.Team', related_name='ngo_focus_teams', null=True, blank=True)
    contact_person_bio = models.TextField(blank=True, null=True)

class SocialMedia(models.Model):
    ngo = models.ForeignKey(NGOEntity, related_name="social_media", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('user.CustomUser', related_name="user_social_media", on_delete=models.CASCADE, null=True, blank=True)
    platform = models.CharField(max_length=50, choices=SocialMedia.choices)
    url = models.URLField()

class Contact(models.Model):
    ngo = models.ForeignKey(NGOEntity, related_name="contact_options", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('user.CustomUser', related_name="user_contact_options", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)  
    contact_type = models.CharField(max_length=20, choices=ContactType.choices)
    contact_info = models.CharField(max_length=100)
