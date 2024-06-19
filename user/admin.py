from django.contrib import admin
from .models import CustomUser, Week, WeeklyUserStats, UserStreak, Team, Competences, CompletedEvents, Goal, UserGoal, NGO, Store, UserReview

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Week)
admin.site.register(WeeklyUserStats)
admin.site.register(UserStreak)
admin.site.register(Team)
admin.site.register(Competences)
admin.site.register(CompletedEvents)
admin.site.register(Goal)
admin.site.register(UserGoal)
admin.site.register(NGO)
admin.site.register(Store)
admin.site.register(UserReview)