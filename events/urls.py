from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('api/events/', views.getEvents),
    path('api/mapmarkers/', views.getMapMarkers),
    path('api/events/create/', views.createEvent),
    path('api/events/<int:pk>/update/', views.updateEvent),
    path('api/events/<int:pk>/delete/', views.deleteEvent),
    path('api/events/<int:pk>/', views.getEvent)
]
