from django.db import models

class Competences(models.Model):
    name = models.TextField()
    description = models.TextField()

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    text = models.TextField()

class Team(models.Model):
    name = models.TextField()


