from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from ngo.models import NGOEntity
from shared.models import Competences, Location, Team
from events.models import Event

class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):

    username = None  # Identify user by email instead of username
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    total_xp = models.PositiveIntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_image_url = models.URLField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    number_top_finishes = models.PositiveIntegerField(default=0, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', null=True, blank=True)
    focus_teams = models.ManyToManyField(Team, related_name='user_focus_teams', null=True, blank=True)
    gained_competences = models.ManyToManyField(Competences, related_name='user_gained_competences', null=True, blank=True)
    saved_events = models.ManyToManyField(Event, related_name="events_saved_by_user", null=True, blank=True)
    enrolled_events = models.ManyToManyField(Event, related_name="enrolled_in_events", null=True, blank=True)
    applied_events = models.ManyToManyField(Event, related_name="applied_for_events", null=True, blank=True)
    created_events = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name='events_created_by_user')

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

class Week(models.Model):
    LEAGUE_CHOICES = [
        ('Bronze', 'Bronze'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Shell', 'Shell')
        # These need to be changed 
    ]

    start = models.DateField()
    end = models.DateField()
    league = models.CharField(max_length=20, choices=LEAGUE_CHOICES)

    def __str__(self):
        return f"{self.league} Week ({self.start} to {self.end})"

class WeeklyUserStats(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    xp_earned = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Save the current WeeklyUserStats instance
        super().save(*args, **kwargs)
        # Update the user's total XP
        self.user.total_xp = WeeklyUserStats.objects.filter(user=self.user).aggregate(models.Sum('xp_earned'))['xp_earned__sum'] or 0
        self.user.save()

    def __str__(self):
        return f"{self.user.username} - {self.week} - XP: {self.xp_earned}, Rank: {self.rank}"

class UserStreak(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_streak_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Current Streak: {self.current_streak}, Longest Streak: {self.longest_streak}"

class Goal(models.Model):
    name = models.TextField()
    description = models.TextField()
    level = models.IntegerField()
    xp_required = models.IntegerField()

class UserGoal(models.Model):
    STATUS_CHOICES = [
        (1, 1),
        (2, 2),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    xp_accumulated = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'status',)

class CompletedEvents(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="completed_event")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="completed_event")
    date_completed = models.DateField(auto_now=True)

class Store(models.Model):
    about = models.TextField()
    followers = models.ManyToManyField(CustomUser, related_name='store_followers')
    rating = models.IntegerField(default=0)
    store_goal = models.TextField()
    product_desc = models.TextField()
    store_location = models.OneToOneField(Location, on_delete=models.CASCADE)

class Post(models.Model):
    description = models.TextField(null=True, blank=True)
    post_image = models.URLField(null=True, blank=True)
    created_by_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_by_ngo = models.ForeignKey(NGOEntity, on_delete=models.CASCADE, null=True, blank=True)

class UserReview(models.Model):
    user_reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    reviewed_ngo = models.OneToOneField(NGOEntity, on_delete=models.CASCADE, null=True, blank=True)
    reviewed_store = models.OneToOneField(Store, on_delete=models.CASCADE, null=True, blank=True)
    review_comment = models.TextField()
    reviewed_rating = models.FloatField()
    date_reviewed = models.DateField()

class Product(models.Model):
    name = models.TextField()
    product_image = models.URLField(blank=True, null=True)
    description = models.TextField()
