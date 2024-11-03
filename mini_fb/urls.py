## mini_fb/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from .views import ShowAllView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusMessageView, CreateFriendView, ShowFriendSuggestionsView, ShowNewsFeedView
from django.contrib.auth import views as auth_views

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
    path('profile/<int:pk>/add_friend/<int:other_pk>', CreateFriendView.as_view(), name='add_friend'), ## add a friend
    path('profile/<int:pk>/friend_suggestions', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'), ## show friend suggestions
    path('profile/<int:pk>/news_feed', ShowNewsFeedView.as_view(), name='news_feed'), ## show news feed
    path('logout', auth_views.LogoutView.as_view(next_page='show_all_profiles'), name='mini_fb_logout'),
]