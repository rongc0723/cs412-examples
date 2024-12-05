## project/urls.py
## descrption: the app-specific URLS for the project application

from django.urls import path
from django.conf import settings
from .views import ShowAllItemsView, ShowItemView, CreatePostingView, ShowAllUsersView, ShowUserView, ShowPersonalProfileView
from django.contrib.auth import views as auth_views


# create a list of urls for this app:
urlpatterns = [
    path('', ShowAllItemsView.as_view(), name='show_all_items'),
    path('show_item/<int:pk>', ShowItemView.as_view(), name='show_item'),
    path('create_posting/', CreatePostingView.as_view(), name='create_posting'),
    path('show_all_users', ShowAllUsersView.as_view(), name='show_all_users'),
    path('show_user/<int:pk>', ShowUserView.as_view(), name='show_user'),
    path('profile/', ShowPersonalProfileView.as_view(), name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_items'), name='project_logout'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='project_login'),
]