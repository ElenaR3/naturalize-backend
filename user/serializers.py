import importlib
from rest_framework import serializers
from events.serializers import TeamSerializer
from shared.serializers import PhotoSerializer
from shared.models import Location
from .models import Donation, Goal, NGOEntity, CustomUser, Petition, Post, UserGoal
from rest_framework.serializers import ModelSerializer
from shared.serializers import AchievementsSerializer, CompetencesSerializer
from django.db.models import QuerySet

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "email", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create(email=validated_data['email'],
                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserPostSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('name', 'surname')

class PostSerializer(ModelSerializer):
    created_by_user = UserPostSerializer()
    class Meta:
        model = Post()
        fields = '__all__'

# class NGOProfileSerializer(ModelSerializer):
#     ngo_profile_gallery = PhotoSerializer(many=True)

#     def get_focus_teams(self, obj):
#         # Using importlib to import TeamSerializer lazily
#         TeamSerializer = importlib.import_module('events.serializers').TeamSerializer
#         return TeamSerializer(obj.focus_teams, many=True).data

#     class Meta:
#         model = NGOEntity()
#         fields = '__all__'

class UserStatsSerializer(serializers.Serializer):
    xp_earned = serializers.IntegerField()
    rank = serializers.IntegerField()

class UserXPSerializer(serializers.Serializer):
    total_xp = serializers.IntegerField()
    number_top_finishes = serializers.IntegerField()

class UserStreakSerializer(serializers.Serializer):
    current_streak = serializers.IntegerField()

class UserProfileSerializer(ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    gained_competences = CompetencesSerializer(many=True, read_only=True)
    gallery_photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["name", "surname", "following", "followers", "bio", "focus_teams", "gallery_photos",
        "gained_competences"]

    def get_following(self, obj):
        return obj.following.count()

    def get_followers(self, obj):
        return obj.followers.count()

class FriendsAppliedSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "name", "surname", "profile_image_url"]

class PetitionSerializer(ModelSerializer):
    is_saved = serializers.SerializerMethodField()
    impact_gallery = PhotoSerializer()

    class Meta:
        model = Petition 
        fields = ["id", "is_saved", "title","avg_rating","xp_given","start_date","about","friends_that_signed","image_url","about_creator",
    "total_signs","created_by","impact_gallery"]
      
    def get_is_saved(self, obj):
        user = self.context.get('user')
        return user.saved_user_petitions.filter(id=obj.id).exists()

class DonationSerializer(ModelSerializer):
    
    location = LocationSerializer()
    is_saved = serializers.SerializerMethodField() 
    impact_gallery = PhotoSerializer()

    class Meta:
        model = Donation 
        fields = ["id", "is_saved", "title","avg_rating","xp_given","start_date","about","friends_that_donated","image_url","about_creator",
    "impact_gallery", "location"]
    
    def get_is_saved(self, obj):
        user = self.context.get('user')
        return user.saved_donations_by_users.filter(id=obj.id).exists()

class GoalSerializer(ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__' 

class UserGoalSerializer(ModelSerializer):
    goal = GoalSerializer()

    class Meta:
        model = UserGoal
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    gained_competences = CompetencesSerializer(many=True, read_only=True)
    gained_achievements = AchievementsSerializer(many=True, read_only=True)
    gallery_photos = PhotoSerializer(many=True, read_only=True)  # Related to the CustomUser (user_profile_gallery)
    created_events = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "email", "name", "surname", "total_xp", "profile_image_url", 
            "bio", "birthday", "number_top_finishes", "following", 
            "followers", "gained_competences", "gained_achievements", "gallery_photos", "created_events"
        ]

    def get_following(self, obj):
        # Return the count of following users
        return obj.following.count()

    def get_followers(self, obj):
        # Return the count of followers
        return obj.followers.count()

    def get_created_events(self, obj):
        # due to circular import 
        from events.serializers import EventSerializer
        events = obj.created_events.all() if isinstance(obj.created_events, QuerySet) else [obj.created_events]
        return EventSerializer(events, many=True).data if events else []

class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'total_xp', 'profile_image_url', 
                  'birthday', 'bio', 'number_top_finishes','focus_teams']