from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView, CreateView
from .models import Item


class ShowAllItemsView(ListView):
    model = Item

    context_object_name = 'items'

    template_name = 'project/show_all_items.html'

class ShowItemView(DetailView):
    model = Item
    template_name = 'project/show_item.html'
    context_object_name = 'item'