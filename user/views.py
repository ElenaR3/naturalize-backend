# Create your views here.
from django.utils import timezone
from pstats import Stats, StatsProfile
import statistics
from rest_framework.views import APIView

from user.models import CustomUser, Season, UserStats, UserStreak
from .serializers import UserSerializer, UserStatsSerializer, UserStreakSerializer, UserXPSerializer
from rest_framework.response import Response


# view for registering users
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserStatsView(APIView):
    def get(self, request, user_id):
        # Get the current date
        current_date = timezone.now()
        
        # Find the current season based on the current date
        current_season = Season.objects.filter(start__lte=current_date, end__gte=current_date).first()

        if current_season:
            # Retrieve UserStats data for the user and the current season
            user_stats = UserStats.objects.filter(user_id=user_id, season=current_season).first()
            user_streak = UserStreak.objects.filter(user_id=user_id).first()
            user = CustomUser.objects.filter(pk=user_id).first()
            
            user_stats_serializer = UserStatsSerializer(user_stats)
            user_streak_serializer = UserStreakSerializer(user_streak)
            custom_user_serializer = UserXPSerializer(user)

            # Combine both serializer data into a single dictionary
            serialized_data = {
                  'user_stats': user_stats_serializer.data,
                  'streak_data': user_streak_serializer.data,  # Extract current_streak from serializer data
                  'userxp': custom_user_serializer.data
            }
            return Response(serialized_data)
        else:
            return Response({'error': 'UserStats not found'}, status=StatsProfile.HTTP_404_NOT_FOUND)