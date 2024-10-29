## blog/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from .views import ShowAllView, RandomArticleView, ArticlePageView, CreateCommentView, CreateArticleview, UpdateArticleView, DeleteCommentView
from django.contrib.auth import views as auth_views


# create a list of urls for this app:
urlpatterns = [
    path('', RandomArticleView.as_view(), name='random'),
    path('show_all', ShowAllView.as_view(), name='show_all'),
    path('article/<int:pk>', ArticlePageView.as_view(), name='article'),
    # path('create_comment', CreateCommentView.as_view(), name='create_comment'),
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'),
    path('create_article', CreateArticleview.as_view(), name='create_article'),
    path('article/<int:pk>/update_article', UpdateArticleView.as_view(), name='update_article'),
    path('delete_comment/<int:pk>', DeleteCommentView.as_view(), name='delete_comment'),
    # authentication urls
    path('login', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'), ## NEW
]