from multiprocessing import Event
from rest_framework import serializers

from shared.models import Competences
from .models import NGOEntity, CustomUser, Post
from rest_framework.serializers import ModelSerializer

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


class UserEventsCalendar(ModelSerializer):
    enrolled_events = UserSerializer(many=True)
    applied_events = UserSerializer(many=True)
    saved_events = UserSerializer(many=True)
    class Meta:
        model = Event
        fields = '__all__'

class UserStatsSerializer(serializers.Serializer):
    xp_earned = serializers.IntegerField()
    rank = serializers.IntegerField()

class UserXPSerializer(serializers.Serializer):
    total_xp = serializers.IntegerField()
    number_top_finishes = serializers.IntegerField()

class UserStreakSerializer(serializers.Serializer):
    current_streak = serializers.IntegerField()

class NGOProfileSerializer(ModelSerializer):
    class Meta:
        model = NGOEntity()
        fields = '__all__'