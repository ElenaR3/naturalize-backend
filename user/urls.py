from django.urls import path
from user.views import GetAllEvents, GetDonations, GetPetitions, RegisterView, UserFeed, UserStatsView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name="sign_up"),
    path('api/userStats/', UserStatsView.as_view(), name="weekly_user_stats"),
    path('api/feed/', UserFeed.as_view(), name="user_feed"),
    path('api/events', GetAllEvents.as_view(), name="user_events"),
    path('api/users/userProfile/<int:user_id>', views.get_user_profile, name="user_profile"),
    path('api/petitions', GetPetitions.as_view(), name="user_petitions"),
    path('api/donations', GetDonations.as_view(), name="user_donations"),
    path('api/users/<int:user_id>/events/<int:event_id>/apply/', views.apply_to_event, name='apply-to-event'),
    path('api/users/<int:user_id>/events/<int:event_id>/save/', views.save_event, name='save_event'),
    path('api/users/<int:user_id>/events/', views.get_user_events, name='get-user=events'),
    path('api/users/edit/', views.edit_user_profile, name="edit-user-profile"),
    path('api/users/active-goal/<int:user_id>', views.get_user_active_goal, name="get-user-active-goal"),
    path('api/users/animal-collection', views.get_animal_collection, name="animal-collection")
]