## formdata/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views


# create a list of urls for this app:
urlpatterns = [
    path('', views.show_form, name='show_form'), ## main page
    path('submit/', views.submit, name='submit'), ## submit page
]