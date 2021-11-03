"""
URLs для приложения places
"""
from django.urls import path
from .views import start_page, get_place_info

urlpatterns = [
    path('places/<int:pk>', get_place_info),
    path('', start_page),
]
