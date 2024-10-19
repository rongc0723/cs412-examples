from django.shortcuts import render

# Create your views here.
from .models import Article
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .forms import CreateCommentForm, CreateArticleForm, UpdateArticleForm
from django.urls import reverse
import random
from typing import Any
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

class CreateCommentView(CreateView):
    ''' A view to create a new comment and save to db'''
    form_class = CreateCommentForm
    template_name = 'blog/create_comment_form.html'

    def form_valid(self, form):
        '''Handle submmission, needs to set foreign key
        by attaching article to the comment object
        can find the article pk in url'''
        print(form.cleaned_data)
        article = Article.objects.get(pk=self.kwargs['pk'])
        form.instance.article = article
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('article', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''build dict of context data for the view'''
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        context['article'] = article
        return context 

class CreateArticleview(CreateView):
    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'
    def form_valid(self, form):
        return super().form_valid(form)

class UpdateArticleView(UpdateView):
    form_class = UpdateArticleForm
    template_name = 'blog/update_article_form.html'
    model = Article
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''build dict of context data for the view'''
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        context['article'] = article
        return context