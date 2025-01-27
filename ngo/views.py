from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ngo.models import NGOEntity
from ngo.serializers import NGOProfileSerializer

@api_view(['GET'])
def getNGOProfile(request, ngo_id):
    try:
        ngo_profile = NGOEntity.objects.get(id=ngo_id)
        serializer = NGOProfileSerializer(ngo_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except NGOEntity.DoesNotExist:
        return Response({"error": "NGO Profile does not exist."}, status=status.HTTP_404_NOT_FOUND)  