from typing import Any
from django.forms import BaseModelForm
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Item, Profile, Image
from django.db.models import Model

# Create your views here.

from django.views.generic import ListView, DetailView, CreateView
from .models import Item
from .forms import CreateItemForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ShowAllItemsView(ListView):
    model = Item

    context_object_name = 'items'

    template_name = 'project/show_all_items.html'

    def get_queryset(self):
        qs = super().get_queryset().order_by('-timestamp')
        qs = qs.filter(is_sold=False)
        if self.request.GET.get('include_sold') == 'on':
            qs = Item.objects.all()
        if 'sort_by' in self.request.GET:
            sort_by = self.request.GET['sort_by']
            if sort_by == 'price_asc':
                qs = qs.order_by('price')
            elif sort_by == 'price_desc':
                qs = qs.order_by('-price')
            elif sort_by == 'date_new':
                qs = qs.order_by('-timestamp')
            elif sort_by == 'date_old':
                qs = qs.order_by('timestamp')
        return qs
            

class ShowItemView(DetailView):
    model = Item
    template_name = 'project/show_item.html'
    context_object_name = 'item'

class ShowAllUsersView(ListView):
    model = Profile

    context_object_name = 'users'

    template_name = 'project/show_all_users.html'

class ShowUserView(DetailView):
    model = Profile
    template_name = 'project/show_user.html'
    context_object_name = 'user'

class ShowPersonalProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'project/show_profile.html'

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

class CreatePostingView(LoginRequiredMixin, CreateView):
    form_class = CreateItemForm
    template_name = 'project/create_posting.html'
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        '''Handle submmission, needs to set foreign key'''
        user = self.request.user
        profile = Profile.objects.get(user=user)
        form.instance.seller = profile
        item = form.save()
        files = self.request.FILES.getlist('files')
        for f in files:
            Image.objects.create(image_file=f, item=item)
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('show_item', kwargs={'pk': self.object.pk})
