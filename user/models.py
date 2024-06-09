from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

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
    total_xp = models.PositiveIntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    surname = models.CharField(max_length=100, null=True, blank=True)
    image_file = models.ImageField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

class Season(models.Model):
    LEAGUE_CHOICES = [
        ('Bronze', 'Bronze'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        # These need to be changed 
    ]

    start = models.DateField()
    end = models.DateField()
    league = models.CharField(max_length=20, choices=LEAGUE_CHOICES)

    def __str__(self):
        return f"{self.league} Season ({self.start} to {self.end})"

class UserStats(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    xp_earned = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Save the current UserStats instance
        super().save(*args, **kwargs)
        # Update the user's total XP
        self.user.total_xp = UserStats.objects.filter(user=self.user).aggregate(models.Sum('xp_earned'))['xp_earned__sum'] or 0
        self.user.save()

    def __str__(self):
        return f"{self.user.username} - {self.season} - XP: {self.xp_earned}, Rank: {self.rank}"

class UserStreak(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_streak_update = models.DateField()

    def __str__(self):
        return f"{self.user.username} - Current Streak: {self.current_streak}, Longest Streak: {self.longest_streak}"

class StreakSnapshot(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    weekly_xp = models.PositiveIntegerField(default=0)
    streak_date = models.DateField()
    final_rank = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.streak_date}: Streak {self.streak_length}, Rank {self.final_rank}"


