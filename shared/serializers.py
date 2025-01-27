from rest_framework import serializers

from shared.models import Achievements, Competences, Photo, Team

class TeamSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='get_name_display') 

    class Meta:
        model = Team
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):

    thumbnail = serializers.SerializerMethodField()
    large = serializers.SerializerMethodField()
     
    class Meta:
        model = Photo
        fields = ['id', 'thumbnail', 'large', 'caption']

    def get_thumbnail(self, obj):
    # Assuming the saved URL format is "https://i.imgur.com/abc123.jpg"
        return obj.image

    def get_large(self, obj):
        # Adding 'l' before the file extension
        if obj.image:
            parts = obj.image.rsplit('.', 1)  # Split at the last dot
            if len(parts) == 2:
                return f"{parts[0]}l.{parts[1]}"  # Add 'l' to the base URL
        return None

class AchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = '__all__'

class CompetencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competences
        fields = '__all__'