from django.urls import path
from .admin_ngo import ngo_admin_site 

from . import views

urlpatterns = [
    path('api/organizations/ngo-profile/<int:ngo_id>', views.getNGOProfile, name='ngo-profile'),
    path('ngo-admin/', ngo_admin_site.urls), 
]
