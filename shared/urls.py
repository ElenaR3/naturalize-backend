from django.urls import path
from . import views

urlpatterns = [
    path('api/users/photos/upload', views.upload_photo_user, name='photo-upload-users'),
    path('api/ngo/photos/upload', views.upload_photo_ngo, name='photo-upload-ngos'),
    path('api/event/photos/upload', views.upload_photo_event, name='photo-upload-event'),
]
