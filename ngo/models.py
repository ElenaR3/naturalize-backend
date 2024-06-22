from django.db import models

# Create your models here.

class NGOEntity(models.Model):
    name = models.TextField()
    about = models.TextField()
    profile_image_url = models.URLField(null=True, blank=True)
    volonteer_num = models.IntegerField(default=0)
    avg_rating = models.IntegerField(default=0)
    total_ratings = models.IntegerField(default=0)
    total_xp = models.IntegerField(default=0)