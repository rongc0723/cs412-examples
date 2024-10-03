from django.shortcuts import render

# Create your views here.
from .models import Article
from django.views.generic import ListView

class ShowAllView(ListView):
    model = Article

    template_name = 'blog/show_all.html'
    context_object_name = 'articles'