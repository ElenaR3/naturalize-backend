# your_app/utils.py
from django.db import transaction
from django.core.exceptions import ValidationError

from django.db import transaction
from django.core.exceptions import ValidationError

def add_xp_to_user(user, xp_earned):
    """
    Adds XP to the user and updates their stage progress if necessary.
    """
    if xp_earned < 0:
        raise ValidationError("XP earned must be a positive value.")

    with transaction.atomic():
        user.total_xp += xp_earned

        # Check if the user can progress to the next stage
        current_stage = user.current_stage
        if current_stage and user.xp_earned >= current_stage.xp_required:
            next_stage = current_stage.next_stage
            if next_stage:
                user.current_stage = next_stage
            else:
                # User has completed all stages, what should happen here?
                user.current_stage = None

        # Save the updated user
        user.save()