from django.contrib import admin

from shared.models import Competences, Location, Team, Photo

# Register your models here.

admin.site.register(Location)
admin.site.register(Team)
admin.site.register(Competences)
admin.site.register(Photo)