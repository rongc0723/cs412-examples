## hw/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views


# create a list of urls for this app:
urlpatterns = [
    #path(url, view, name)
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]
