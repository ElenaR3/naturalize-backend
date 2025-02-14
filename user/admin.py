from django.contrib import admin

from .models import CustomUser, Donation, Petition, ExperienceDevelopmentStage, Week, Post, WeeklyUserStats, UserStreak, CompletedEvents, Goal, UserGoal, Store, UserReview, Product, UserEventInteraction

admin.site.register(CustomUser)
admin.site.register(Week)
admin.site.register(WeeklyUserStats)
admin.site.register(UserStreak)
admin.site.register(CompletedEvents)
admin.site.register(Goal)
admin.site.register(UserGoal)
admin.site.register(Store)
admin.site.register(UserReview)
admin.site.register(Product)
admin.site.register(Post)
admin.site.register(Donation)
admin.site.register(Petition)
admin.site.register(UserEventInteraction)
admin.site.register(ExperienceDevelopmentStage)