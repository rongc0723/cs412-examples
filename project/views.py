from typing import Any
from django.forms import BaseModelForm
from django.db.models import QuerySet
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Item, Profile, Image
from django.db.models import Model
from django.http import Http404
import plotly
import plotly.graph_objs as go
from collections import defaultdict

# Create your views here.

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Item
from .forms import CreateItemForm, UpdateListingForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateProfileForm, UpdateProfileForm
from django.contrib.auth import login
from django.shortcuts import redirect


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

    context_object_name = 'profiles'

    template_name = 'project/show_all_users.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = sorted(qs, key=lambda obj: obj.get_ratings(), reverse=True)
        return qs

class ShowUserView(DetailView):
    model = Profile
    template_name = 'project/show_user.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        # get all items that the user is selling
        items = Item.objects.filter(seller=profile)
        sold_items = items.filter(is_sold=True).order_by('-timestamp')
        sale_items = items.filter(is_sold=False).order_by('-timestamp')

        context['sold_items'] = sold_items
        context['sale_items'] = sale_items

        # plot the ratings
        reviews = profile.review_set.all()
        ratings = [review.rating for review in reviews]

        rating_counts = defaultdict(int)
        for rating in ratings:
            rating_counts[rating] += 1
        
        for i in range(6):
            if i not in rating_counts:
                rating_counts[i] = 0
        y = list(range(6))
        x = [rating_counts[rating] for rating in y]
        
        fig = go.Figure(go.Bar(x=x, y=y, orientation='h'))

        fig.update_layout(
            width=400,
            height=300,
            title="Ratings",
            xaxis_title="Count",
            yaxis_title="Rating",
            yaxis=dict(
                tickmode='array',
                tickvals=y,
                ticktext=[str(i) for i in y],
            )
        )
        bar_div = plotly.offline.plot({'data': fig.data, 'layout': fig.layout}, auto_open=False, output_type='div')
        context['bar_div'] = bar_div

        return context

class ShowPersonalProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'project/show_profile.html'

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        # get all items that the user is selling
        user = self.request.user
        profile = Profile.objects.get(user=user)
        items = Item.objects.filter(seller=profile)
        sold_items = items.filter(is_sold=True).order_by('-timestamp')
        sale_items = items.filter(is_sold=False).order_by('-timestamp')

        context['sold_items'] = sold_items
        context['sale_items'] = sale_items

        # plot the ratings
        reviews = profile.review_set.all()
        ratings = [review.rating for review in reviews]

        rating_counts = defaultdict(int)
        for rating in ratings:
            rating_counts[rating] += 1
        
        for i in range(6):
            if i not in rating_counts:
                rating_counts[i] = 0
        y = list(range(6))
        x = [rating_counts[rating] for rating in y]
        
        fig = go.Figure(go.Bar(x=x, y=y, orientation='h'))

        fig.update_layout(
            width=400,
            height=300,
            title="Ratings",
            xaxis_title="Count",
            yaxis_title="Rating",
            yaxis=dict(
                tickmode='array',
                tickvals=y,
                ticktext=[str(i) for i in y],
            )
        )
        bar_div = plotly.offline.plot({'data': fig.data, 'layout': fig.layout}, auto_open=False, output_type='div')
        context['bar_div'] = bar_div

        return context

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

class CreateProfileView(CreateView):
    ''' A view to create a new profile and save to db'''
    form_class = CreateProfileForm
    template_name = 'project/create_profile_form.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        print("get context data")
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            user_form = UserCreationForm
            context['user_form'] = user_form
        return context
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        print("form is invalid")
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        print("form is valid")
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            print(profile)
            login(self.request, user)
            return redirect(reverse('profile'))
        else:
            return render(self.request, self.template_name, {'form': form, 'user_form': user_form})

    def get_success_url(self):
        return reverse('show_all_users')
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    form_class = UpdateProfileForm
    template_name = 'project/edit_profile.html'
    model = Profile
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

    def get_success_url(self):
        return reverse('profile')

class UpdateListingView(UserPassesTestMixin, UpdateView):
    model = Item
    form_class = UpdateListingForm
    template_name = 'project/edit_listing.html'
    context_object_name = 'item'

    def test_func(self) -> bool | None:
        item = self.get_object()
        return item.seller.user == self.request.user

    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'project/no_permission.html', {
            'message': "You are not authorized to edit this listing."
        })

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        item = form.save()
        item.image_set.all().delete()
        files = self.request.FILES.getlist('files')
        for f in files:
            Image.objects.create(image_file=f, item=item)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_item', kwargs={'pk': self.object.pk})



