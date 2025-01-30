from rest_framework import serializers

from ngo.models import NGOEntity
from shared.serializers import PhotoSerializer, TeamSerializer, UserReviewSerializer, SocialMediaSerializer, ContactSerializer

class NGOProfileSerializer(serializers.ModelSerializer):

    focus_teams = TeamSerializer(many=True)
    user_reviews = UserReviewSerializer(many=True, read_only=True)
    social_media = SocialMediaSerializer(many=True, read_only=True)
    contact_options = ContactSerializer(many=True, read_only=True)
    ngo_profile_gallery = PhotoSerializer(many=True, read_only=True, source="ngo_personal_gallery")

    class Meta:
        model = NGOEntity
        fields = '__all__'