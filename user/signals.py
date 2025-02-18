from django.db.models.signals import post_save, post_delete
from django.db import models
from django.dispatch import receiver
from .models import WeeklyUserStats, UserEventInteraction, CustomUser, Goal, UserGoal
from django.core.mail import send_mail
from django.template.loader import render_to_string


@receiver(post_save, sender=WeeklyUserStats)
def update_total_xp_on_save(sender, instance, **kwargs):
    instance.user.total_xp = WeeklyUserStats.objects.filter(user=instance.user).aggregate(models.Sum('xp_earned'))['xp_earned__sum'] or 0
    instance.user.save()

@receiver(post_delete, sender=WeeklyUserStats)
def update_total_xp_on_delete(sender, instance, **kwargs):
    instance.user.total_xp = WeeklyUserStats.objects.filter(user=instance.user).aggregate(models.Sum('xp_earned'))['xp_earned__sum'] or 0
    instance.user.save()

@receiver(post_save, sender=UserEventInteraction)
def send_email_on_status_change(sender, instance, **kwargs):
    if instance.status == 'applied':
        subject = f'New Application for Event: {instance.event.eventName}'
        message = render_to_string('user/emails/new_application_email.txt', {
            'event': instance.event,
            'user': instance.user,
        })
        send_mail(
            subject,
            message,
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )

    if instance.status == 'accepted':
        subject = f'Your Application Has Been Accepted: {instance.event.eventName}'
        message = render_to_string('user/emails/application_accepted_email.txt', {
            'event': instance.event,
            'user': instance.user,
        })
        send_mail(
            subject,
            message,
            'greenie@gmail.com',
            [instance.user.email],
            fail_silently=False,
        )


@receiver(post_save, sender=CustomUser)
def assign_default_goal(sender, instance, created, **kwargs):
    if created: 
        default_goal = Goal.objects.first()
        if default_goal:
            first_stage = default_goal.stages.order_by("min_xp").first()

            UserGoal.objects.create(
                user=instance,
                goal=default_goal,
                current_stage=first_stage,
                xp_accumulated=0
            )