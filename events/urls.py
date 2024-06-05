from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('events/', views.getEvents),
    path('events/create/', views.createEvent),
    path('events/<int:pk>/update/', views.updateEvent),
    path('events/<int:pk>/delete/', views.deleteEvent),
    path('events/<int:pk>/', views.getEvent)
]
