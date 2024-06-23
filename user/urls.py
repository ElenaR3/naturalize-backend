from django.urls import path
from user.views import GetAllEvents, GetUserProfile, RegisterView, UserFeed, UserStatsView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name="sign_up"),
    path('api/userStats/', UserStatsView.as_view(), name="weekly_user_stats"),
    path('api/feed/', UserFeed.as_view(), name="user_feed"),
    path('api/events', GetAllEvents.as_view(), name="user_events"),
    path('api/userProfile', GetUserProfile.as_view(), name="user_profile")
]