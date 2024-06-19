from django.contrib import admin

# Register your models here.

from .models import Achievements, Event, Location

admin.site.register(Event) # show table in Django admin panel
admin.site.register(Location)
admin.site.register(Achievements)