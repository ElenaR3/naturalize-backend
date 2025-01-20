from rest_framework import serializers

from shared.models import Photo

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
