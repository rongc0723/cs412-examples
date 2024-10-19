## mini_fb/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from .views import ShowAllView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusMessageView

# app_name = 'mini_fb'

# create a list of urls for this app:
urlpatterns = [
    path('', ShowAllView.as_view(), name='show_all_profiles'), ## main page
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'), ## show one profile
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'), ## create a new profile
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'), ## create a new status message
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'), ## update a profile
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'), ## delete a status message
    path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'), ## update a status message
]