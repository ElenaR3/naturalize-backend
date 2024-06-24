from rest_framework import serializers

from shared.models import Competences, Location
from .models import Donation, Goal, NGOEntity, CustomUser, Petition, Post, UserGoal, UserPhoto, Photo
from rest_framework.serializers import ModelSerializer

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "email", "name", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create(email=validated_data['email'],
                                       name=validated_data['name']
                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserPostSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('name', 'surname')

class CompetencesSerializer(ModelSerializer):
    class Meta:
        model = Competences()
        fields = '__all__'

class PostSerializer(ModelSerializer):
    created_by_user = UserPostSerializer()
    class Meta:
        model = Post()
        fields = '__all__'

class NGOProfileSerializer(ModelSerializer):
    class Meta:
        model = NGOEntity()
        fields = '__all__'

class UserStatsSerializer(serializers.Serializer):
    xp_earned = serializers.IntegerField()
    rank = serializers.IntegerField()

class UserXPSerializer(serializers.Serializer):
    total_xp = serializers.IntegerField()
    number_top_finishes = serializers.IntegerField()

class UserStreakSerializer(serializers.Serializer):
    current_streak = serializers.IntegerField()

class UserPhotoSerializer(ModelSerializer):
    class Meta:
        model = UserPhoto 
        fields = ['image', 'caption']

class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo 
        fields = ['image', 'caption']

class UserProfileSerializer(ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    gained_competences = CompetencesSerializer(many=True, read_only=True)
    gallery_photos = UserPhotoSerializer(many=True)

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