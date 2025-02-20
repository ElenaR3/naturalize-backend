from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
from user.models import UserStreak

class Command(BaseCommand):
    help = "Resets streaks for users who have been inactive since yesterday."

    def handle(self, *args, **kwargs):
        yesterday = now().date() - timedelta(days=1)

        users_to_reset = UserStreak.objects.filter(last_active_date__lt=yesterday, current_streak__gt=0)
        count = users_to_reset.update(current_streak=0)

        self.stdout.write(self.style.SUCCESS(f"Streaks reset for {count} users."))
