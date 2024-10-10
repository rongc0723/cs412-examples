from django.shortcuts import render

# Create your views here.
from .models import Article
from django.views.generic import ListView, DetailView
import random
class ShowAllView(ListView):
    model = Article

    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

class RandomArticleView(DetailView):
    '''Show the details for one article'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
    def get_object(self):
        '''Return a random article'''
        return random.choice(Article.objects.all())
    
class ArticlePageView(DetailView):
    ''' Show the details for one article'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'