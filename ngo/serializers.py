from rest_framework import serializers

from ngo.models import NGOEntity
from shared.serializers import PhotoSerializer, UserReviewSerializer, SocialMediaSerializer, ContactSerializer

class NGOProfileSerializer(serializers.ModelSerializer):

    focus_teams = serializers.SerializerMethodField()
    user_reviews = UserReviewSerializer(many=True, read_only=True)
    social_media = SocialMediaSerializer(many=True, read_only=True)
    contact_options = ContactSerializer(many=True, read_only=True)
    ngo_profile_gallery = PhotoSerializer(many=True, read_only=True, source="ngo_personal_gallery")
    profile_image_url = serializers.URLField(source='ngo_profile_pictures.first.image', required=False)

    class Meta:
        model = NGOEntity
        fields = '__all__'

    def get_focus_teams(self, obj):
        teams = obj.focus_teams.all()
        return [team.get_name_display() for team in teams]

    # def get_profile_picture(self, obj):
    #     profile_picture = obj.ngo_profile_pictures.first()
    #     if profile_picture and profile_picture.image:
    #         return profile_picture.image
    #     return None  # If no profile picture exists, return None