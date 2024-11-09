
## voter_analytics/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from .views import VotersListView

# create a list of urls for this app:
urlpatterns = [
    path('', VotersListView.as_view(), name='voters'), ## main page
]