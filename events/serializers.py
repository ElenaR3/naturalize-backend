from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import Event, Location

class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ('latitude', 'longitude')

class MapMarkerSerializer(ModelSerializer):
    location = LocationSerializer() # nested serializer
    class Meta:
        model = Event
        fields = ['id', 'eventName', 'markerType', 'eventDescription', 'location', 'team']
