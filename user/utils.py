# your_app/utils.py

from django.db import transaction
from django.core.exceptions import ValidationError

def add_xp_to_user(user, xp_earned):
    if xp_earned == 0:
        return
    elif xp_earned < 0:
            raise ValidationError("XP earned must be a positive value.")

    user_goal = user.usergoal_set.filter(status=1).order_by('-xp_accumulated').first()
    if user_goal:
        print(user_goal.xp_accumulated)

    with transaction.atomic():
        user.total_xp += xp_earned
        user_goal.xp_accumulated += xp_earned
        user.save(update_fields=["total_xp"])
        user_goal.save(update_fields=["xp_accumulated"])

        while user.current_stage and user.total_xp > user.current_stage.xp_required:
            next_stage = user.current_stage.next_stage
            if next_stage:
                user.current_stage = next_stage
                user.save(update_fields=["current_stage"])  # Prevent full save
            else:
                break
