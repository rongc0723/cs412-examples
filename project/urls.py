## project/urls.py
## descrption: the app-specific URLS for the project application

from django.urls import path
from django.conf import settings
from .views import ShowAllItemsView, ShowItemView, CreatePostingView, ShowAllSellersView, ShowSellerView


# create a list of urls for this app:
urlpatterns = [
    path('', ShowAllItemsView.as_view(), name='show_all_items'),
    path('show_item/<int:pk>', ShowItemView.as_view(), name='show_item'),
    path('create_posting/', CreatePostingView.as_view(), name='create_posting'),
    path('show_all_sellers', ShowAllSellersView.as_view(), name='show_all_sellers'),
    path('show_seller/<int:pk>', ShowSellerView.as_view(), name='show_seller'),
]