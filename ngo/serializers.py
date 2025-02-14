from rest_framework import serializers

from ngo.models import NGOEntity
from shared.serializers import PhotoSerializer, UserReviewSerializer, SocialMediaSerializer, ContactSerializer

class NGOProfileSerializer(serializers.ModelSerializer):

    focus_teams = serializers.SerializerMethodField()
    user_reviews = UserReviewSerializer(many=True, read_only=True)
    social_media = SocialMediaSerializer(many=True, read_only=True)
    contact_options = ContactSerializer(many=True, read_only=True)
    ngo_profile_gallery = PhotoSerializer(many=True, read_only=True, source="ngo_personal_gallery")

    class Meta:
        model = NGOEntity
        fields = '__all__'

    def get_focus_teams(self, obj):
        teams = obj.focus_teams.all()
        return [team.get_name_display() for team in teams]