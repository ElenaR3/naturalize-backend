from rest_framework import serializers
from .models import Event, Location, Achievements, Photo
from user.serializers import CompetencesSerializer
from shared.utils import format_datetime
from user.serializers import NGOProfileSerializer, FriendsAppliedSerializer

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class MapMarkerSerializer(serializers.ModelSerializer):
    location = LocationSerializer() # nested serializer
    class Meta:
        model = Event
        fields = ['id', 'eventName', 'markerType', 'eventDescription', 'location', 'team']

class AchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('image', 'caption')

class EventSerializer(serializers.ModelSerializer):
    startDate = serializers.SerializerMethodField()
    endDate = serializers.SerializerMethodField()
    
    location = LocationSerializer()
    gallery_photos = PhotoSerializer(many=True) 
    achievements = AchievementsSerializer(many=True)
    competences = CompetencesSerializer(many=True, read_only=True)
    organized_by = NGOProfileSerializer()

    class Meta:
        model = Event
        fields = '__all__'

    def get_startDate(self, instance):
        return format_datetime(instance.startDate)

    def get_endDate(self, instance):
        return format_datetime(instance.endDate)

class UserEventsCalendar(serializers.ModelSerializer):
    startDate = serializers.SerializerMethodField()
    endDate = serializers.SerializerMethodField()

    location = LocationSerializer()
    gallery_photos = PhotoSerializer(many=True) 
    achievements = AchievementsSerializer(many=True)
    competences = CompetencesSerializer(many=True, read_only=True)
    organized_by = NGOProfileSerializer()

    is_enrolled = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_startDate(self, instance):
        return format_datetime(instance.startDate)

    def get_endDate(self, instance):
        return format_datetime(instance.endDate)

    def get_is_enrolled(self, obj):
        user = self.context.get('user')
        return user.enrolled_events.filter(id=obj.id).exists()

    def get_is_applied(self, obj):
        user = self.context.get('user')
        return user.applied_events.filter(id=obj.id).exists()

    def get_is_saved(self, obj):
        user = self.context.get('user')
        return user.saved_events.filter(id=obj.id).exists()
