## blog/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views
from .views import ShowAllView


# create a list of urls for this app:
urlpatterns = [
    path('', ShowAllView.as_view(), name='show_all')
]