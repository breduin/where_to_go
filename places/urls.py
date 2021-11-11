"""
URLs для приложения places
"""
from django.urls import path
from .views import start_page, get_place_details

urlpatterns = [
    path('place/<int:pk>', get_place_details, name='place_details'),
    path('', start_page),
]
