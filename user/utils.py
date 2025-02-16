# your_app/utils.py

from django.db import transaction
from django.core.exceptions import ValidationError

def add_xp_to_user(user, xp_earned):
    if xp_earned == 0:
        return
    elif xp_earned < 0:
            raise ValidationError("XP earned must be a positive value.")

    with transaction.atomic():
        user.total_xp += xp_earned
        user.save(update_fields=["total_xp"])  # Only update total_xp field

        while user.current_stage and user.total_xp > user.current_stage.xp_required:
            print(f"o m g")
            next_stage = user.current_stage.next_stage
            if next_stage:
                print(f"This is the next stageeee {next_stage}")
                user.current_stage = next_stage
                user.save(update_fields=["current_stage"])  # Prevent full save
            else:
                break
