
## voter_analytics/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from .views import VotersListView, VoterDetailView, GraphsListView

# create a list of urls for this app:
urlpatterns = [
    path('', VotersListView.as_view(), name='voters'), ## main page
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'), ## show all voters
    path('graphs', GraphsListView.as_view(), name='graphs'), ## show all graphs
]