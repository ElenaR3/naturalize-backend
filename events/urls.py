from django.urls import path

from events.serializers import EventListView
from . import views

urlpatterns = [
    path('', views.getRoutes),
    # path('api/events/', views.getEvents),
    # path('api/mapmarkers/', views.getMapMarkers),
    path('api/events/create/', views.createEvent),
    path('api/events/<int:pk>/update/', views.updateEvent),
    path('api/events/<int:pk>/delete/', views.deleteEvent),
    path('api/events/<int:pk>/', views.getEvent),
    path('api/events/', EventListView.as_view(), name='filtered-event-list'),
    path('api/mapmarkers/', EventListView.as_view(), name='filtered-mapmarkers-list'),
    path('api/events/filter_upcoming_events/', views.filter_upcoming_events, name='filter_upcoming_events'),
    path('api/events/filters/', views.get_events_filtering_options, name='get_events_filtering_options'),
    path('api/events/<int:event_id>/gallery/', views.get_event_gallery, name='event-gallery'),
]
