## restaurant/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views


# create a list of urls for this app:
urlpatterns = [
    path('', views.main, name='restaurant_main'), ## main page
    path('order', views.order, name='order'),
    path('confirmation', views.confirmation, name='confirmation'),
]