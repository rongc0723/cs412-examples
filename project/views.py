from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Item, Profile, Image

# Create your views here.

from django.views.generic import ListView, DetailView, CreateView
from .models import Item
from .forms import CreateItemForm


class ShowAllItemsView(ListView):
    model = Item

    context_object_name = 'items'

    template_name = 'project/show_all_items.html'

class ShowItemView(DetailView):
    model = Item
    template_name = 'project/show_item.html'
    context_object_name = 'item'

class ShowAllSellersView(ListView):
    model = Profile

    context_object_name = 'sellers'

    template_name = 'project/show_all_sellers.html'

class ShowSellerView(DetailView):
    model = Profile
    template_name = 'project/show_seller.html'
    context_object_name = 'seller'

class CreatePostingView(CreateView):
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
