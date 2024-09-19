## quotes/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views


# create a list of urls for this app:
urlpatterns = [
    path('', views.home, name='quotes_home'), ## main page
    path('quote/', views.quote, name='quote'), ## quote page
    path('show_all/', views.show_all, name='show_all'), ## show all quotes
    path('about', views.about, name='quotes_about'), ## about page
]