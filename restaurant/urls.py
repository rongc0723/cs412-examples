## restaurant/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views

app_name = 'restaurant'

# create a list of urls for this app:
urlpatterns = [
    path('', views.main, name='main'), ## main page
    path('order', views.order, name='order'),
    path('confirmation', views.confirmation, name='confirmation'),
]