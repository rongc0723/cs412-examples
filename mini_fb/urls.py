## mini_fb/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from .views import ShowAllView

# app_name = 'mini_fb'

# create a list of urls for this app:
urlpatterns = [
    path('', ShowAllView.as_view(), name='show_all_profiles'), ## main page
]