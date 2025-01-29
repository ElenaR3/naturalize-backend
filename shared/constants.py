from django.db import models

class TeamChoices(models.IntegerChoices):
        INTO_THE_HEIGHTS = 1, 'INTO THE HEIGHTS'
        MARINES = 2, 'MARINES'
        GREEN_CITIES = 3, 'GREEN CITIES'
        ANCIENT_FORESTS_FOREVAA = 4, 'ANCIENT FORESTS FOREVAA'

class EventEnrollementStatus(models.TextChoices):
        APPLIED = 'applied', 'Applied'
        ACCEPTED = 'accepted', 'Accepted'
        WAITLISTED = 'waitlisted', 'Waitlisted'
        SAVED = 'saved', 'Saved'

class SocialMedia(models.TextChoices):
        INSTAGRAM = 'Instagram', 'Instagram' 
        LINKEDIN = 'LinkedIn', 'LinkedIn'
        TIKTOK = 'TikTok', 'TikTok'
        FACEBOOK = 'Facebook', 'Facebook'
    
class ContactType(models.TextChoices):
        PHONE_NUMBER = 'Phone', 'Phone'
        MAIL_ADDRESS = 'E-mail', 'E-mail'