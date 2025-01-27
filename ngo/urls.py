from django.urls import path

from . import views

urlpatterns = [
    path('api/events/ngo-profile/<int:ngo_id>', views.getNGOProfile, name='ngo-profile'),
]
