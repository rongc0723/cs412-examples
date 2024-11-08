
## marathon_analytics/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from .views import ResultsListView, ResultDetailView

# create a list of urls for this app:
urlpatterns = [
    path('', ResultsListView.as_view(), name='home'), ## main page
    path('results', ResultsListView.as_view(), name='results'), ## show all results
    path('result/<int:pk>/', ResultDetailView.as_view(), name='result_detail'), ## show all results
]