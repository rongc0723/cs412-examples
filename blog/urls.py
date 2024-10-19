## blog/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from .views import ShowAllView, RandomArticleView, ArticlePageView, CreateCommentView, CreateArticleview


# create a list of urls for this app:
urlpatterns = [
    path('', RandomArticleView.as_view(), name='random'),
    path('show_all', ShowAllView.as_view(), name='show_all'),
    path('article/<int:pk>', ArticlePageView.as_view(), name='article'),
    # path('create_comment', CreateCommentView.as_view(), name='create_comment'),
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'),
    path('create_article', CreateArticleview.as_view(), name='create_article'),
]