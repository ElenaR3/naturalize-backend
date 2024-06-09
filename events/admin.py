from django.contrib import admin

# Register your models here.

from .models import Achievements, Competences, Event, Location

admin.site.register(Event) # show table in Django admin panel
admin.site.register(Location)
admin.site.register(Competences)
admin.site.register(Achievements)