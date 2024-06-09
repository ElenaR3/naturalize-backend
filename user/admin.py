from django.contrib import admin
from .models import CustomUser, Season, UserStats, UserStreak

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Season)
admin.site.register(UserStats)
admin.site.register(UserStreak)