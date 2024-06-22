from django.contrib import admin

# Register your models here.

from .models import Achievements, Event, Photo

admin.site.register(Event) # show table in Django admin panel
admin.site.register(Achievements)
admin.site.register(Photo)