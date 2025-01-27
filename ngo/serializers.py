from multiprocessing import managers
from rest_framework import serializers

from ngo.models import NGOEntity
from shared.serializers import PhotoSerializer, TeamSerializer

class NGOProfileSerializer(serializers.ModelSerializer):

    ngo_profile_gallery = PhotoSerializer(many=True)
    focus_teams = TeamSerializer(many=True)

    class Meta:
        model = NGOEntity
        fields = '__all__'