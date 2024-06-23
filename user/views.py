# Create your views here.
from calendar import week
from django.utils import timezone
from pstats import Stats, StatsProfile
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from events.models import Achievements, Event
from events.serializers import AchievementsSerializer, UserEventsCalendar
from shared.models import Competences
from user.models import CustomUser, Post, WeeklyUserStats, UserStreak, Week, CompletedEvents
from .serializers import CompetencesSerializer, PostSerializer, UserProfileSerializer, UserSerializer, UserStatsSerializer, UserStreakSerializer, UserXPSerializer
from rest_framework.response import Response


# view for registering users
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserStatsView(APIView):
    def post(self, request):
        # Get the current date
        current_date = timezone.now()
        data = request.data
        user_id = data.get('user_id')
        
        # Find the current season based on the current date
        current_week = Week.objects.filter(start__lte=current_date, end__gte=current_date).first()

        if current_week:
            # Retrieve UserStats data for the user and the current season
            user_stats = WeeklyUserStats.objects.filter(user_id=user_id, week=current_week).first()
            user_streak = UserStreak.objects.filter(user_id=user_id).first()
            user = CustomUser.objects.filter(pk=user_id).first()

            #achievements_gained = CompletedEvents.objects.filter(user_id=user_id).select_related('event').prefetch_related('event__achievements')
            achievements_gained = Achievements.objects.filter(event_achv__completed_event__user=user_id).distinct().values('description', 'id', 'name', 'xpGiven')
            competences_gained = Competences.objects.filter(user_gained_competences__id=user_id)

            user_stats_serializer = UserStatsSerializer(user_stats)
            user_streak_serializer = UserStreakSerializer(user_streak)
            custom_user_serializer = UserXPSerializer(user)
            achievements_serializer = AchievementsSerializer(achievements_gained, many=True)
            competences_serializer = CompetencesSerializer(competences_gained, many=True)

            # Combine both serializer data into a single dictionary
            serialized_data = {
                  'current_league': current_week.league,
                  'current_week_xp': user_stats_serializer.data.get('xp_earned'),
                  'current_week_rank': user_stats_serializer.data.get('rank'),
                  'current_streak': user_streak_serializer.data.get('current_streak'),  # Extract current_streak from serializer data
                  'total_xp': custom_user_serializer.data.get('total_xp'),
                  'number_top_finishes': custom_user_serializer.data.get('number_top_finishes'),
                  'user_achievements': achievements_serializer.data,
                  'user_competences': competences_serializer.data
            }
            return Response(serialized_data)
        else:
            return Response({'error': 'WeeklyUserStats not found'}, status=StatsProfile.HTTP_404_NOT_FOUND)

# returns all posts from user's friends
def get_followed_users_posts(user_id):
    # Fetch the user object
    user = CustomUser.objects.get(pk=user_id)
    
    # Get posts created by users that the current user follows
    followed_users_posts = Post.objects.filter(created_by_user__in=user.following.all())

    return followed_users_posts

class UserFeed(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('user_id')

        followed_users_posts = get_followed_users_posts(user_id=user_id)
        serializer = PostSerializer(followed_users_posts, many=True)
        return Response(serializer.data)

class GetUserPlannedEvents(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=Stats.HTTP_404_NOT_FOUND)

        events = Event.objects.all()  # Assuming you want to check all events. Adjust the queryset if needed.

        # Use the serializer with the user context
        serializer = UserEventsCalendar(events, many=True, context={'user': user})

        return Response(serializer.data)

class GetUserProfile(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=Stats.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    

