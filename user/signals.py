from django.db.models.signals import post_save, post_delete
from django.db import models  # Import models module
from django.dispatch import receiver
from .models import WeeklyUserStats

# @receiver(post_save, sender=CustomUser)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

@receiver(post_save, sender=WeeklyUserStats)
def update_total_xp_on_save(sender, instance, **kwargs):
    instance.user.total_xp = WeeklyUserStats.objects.filter(user=instance.user).aggregate(models.Sum('xp_earned'))['xp_earned__sum'] or 0
    instance.user.save()

@receiver(post_delete, sender=WeeklyUserStats)
def update_total_xp_on_delete(sender, instance, **kwargs):
    instance.user.total_xp = WeeklyUserStats.objects.filter(user=instance.user).aggregate(models.Sum('xp_earned'))['xp_earned__sum'] or 0
    instance.user.save()
