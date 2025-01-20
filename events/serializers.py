from rest_framework import serializers
from shared.models import Team
from .models import Event, Location, Achievements, Competences
from user.serializers import CompetencesSerializer
from shared.utils import format_datetime
from user.serializers import NGOProfileSerializer
from rest_framework import generics
from shared.serializers import PhotoSerializer

class TeamSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='get_name_display') 

    class Meta:
        model = Team
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class MapMarkerSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = Event
        fields = ['id', 'eventName', 'markerType', 'eventDescription', 'location', 'team']

class AchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = '__all__'

class CompetencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competences
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    startDate = serializers.SerializerMethodField()
    endDate = serializers.SerializerMethodField()
    main_image_url = serializers.SerializerMethodField()
    
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
    
    def get_main_image_url(self, instance):
        return instance.main_image_url
    
class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = MapMarkerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        team_ids = self.request.query_params.get('team_ids', None)

        if team_ids:
            team_ids_list = []
            for team_id in team_ids.split(','):
                try:
                    team_ids_list.append(int(team_id))
                except ValueError:
                    continue  

            if not team_ids_list:
                return Response({"error": "Invalid team_ids provided"}, status=status.HTTP_400_BAD_REQUEST)

            queryset = queryset.filter(team__id__in=team_ids_list).distinct()

        return queryset

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
