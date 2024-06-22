from django.contrib import admin

from shared.models import Competences, Location, Team

# Register your models here.

admin.site.register(Location)
admin.site.register(Team)
admin.site.register(Competences)