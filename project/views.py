## project/views.py
## descrption: the views for the project application
import datetime
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
from django.db import transaction

# Create your views here.

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Item, Review
from .forms import CreateItemForm, UpdateListingForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateProfileForm, UpdateProfileForm, CreateReviewForm, UpdateReviewForm
from django.contrib.auth import login
from django.shortcuts import redirect


class ShowAllItemsView(ListView):
    '''
    A view to show all items
    '''
    model = Item

    context_object_name = 'items'

    template_name = 'project/show_all_items.html'

    def get_queryset(self):
        ''''
        Get the queryset for this view. Apply filters and sorting based on the request
        '''
        # default queryset is to show all items in reverse chronological order by timestamp
        qs = super().get_queryset().order_by('-timestamp')
        # filter out sold items
        qs = qs.filter(is_sold=False)

        # apply filters based on the request
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
        types = self.request.GET.getlist('type_of_item')
        if types:
            qs = qs.filter(type_of_item__in=types)
        return qs
            

class ShowItemView(LoginRequiredMixin, DetailView):
    '''
    A view to show a single item
    '''
    model = Item
    template_name = 'project/show_item.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        review = item.get_review().first()
        context['review'] = review
        return context
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        ''' Handle the case where the user is not logged in '''
        return render(self.request, 'project/no_permission.html', {
            'message': "Please log in to view this item."
        })

class ShowAllUsersView(ListView):
    ''' A view to show all users '''
    model = Profile

    context_object_name = 'profiles'

    template_name = 'project/show_all_users.html'

    def get_queryset(self):
        ''' Get the queryset for this view. Apply filters and sorting based on the request '''
        qs = super().get_queryset()
        # sort by number of items sold
        qs = sorted(qs, key=lambda obj: obj.get_ratings(), reverse=True)
        # apply filters based on the request
        if 'sort_by' in self.request.GET:
            sort_by = self.request.GET['sort_by']
            if sort_by == 'rating_asc':
                qs = sorted(qs, key=lambda obj: obj.get_ratings())
            elif sort_by == 'rating_desc':
                qs = sorted(qs, key=lambda obj: obj.get_ratings(), reverse=True)
            elif sort_by == 'num_item_asc':
                qs = sorted(qs, key=lambda obj: obj.item_set.count())
            elif sort_by == 'num_item_dsc':
                qs = sorted(qs, key=lambda obj: obj.item_set.count(), reverse=True)
        return qs

class ShowUserView(DetailView):
    ''' Show the details for one user '''
    model = Profile
    template_name = 'project/show_user.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ''' Add additional context like a graph of ratings to the view '''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        # get all items that the user is selling
        items = Item.objects.filter(seller=profile)
        sold_items = items.filter(is_sold=True).order_by('-timestamp')
        sale_items = items.filter(is_sold=False).order_by('-timestamp')

        # add the items to the context
        context['sold_items'] = sold_items
        context['sale_items'] = sale_items

        # gather all ratings
        reviews = profile.review_set.all()
        ratings = [review.rating for review in reviews]

        # count the number of each rating
        rating_counts = defaultdict(int)
        for rating in ratings:
            rating_counts[rating] += 1
        
        # fill in any missing ratings
        for i in range(6):
            if i not in rating_counts:
                rating_counts[i] = 0
        
        # create a bar graph of the ratings
        y = list(range(6))
        x = [rating_counts[rating] for rating in y]
        
        # create the plotly figure
        fig = go.Figure(go.Bar(x=x, y=y, orientation='h'))

        # update the layout
        fig.update_layout(
            width=400,
            height=300,
            title="Seller Ratings",
            xaxis_title="Count",
            yaxis_title="Rating",
            yaxis=dict(
                tickmode='array',
                tickvals=y,
                ticktext=[str(i) for i in y],
            )
        )
        # convert the plotly figure to a div and add to context
        bar_div = plotly.offline.plot({'data': fig.data, 'layout': fig.layout}, auto_open=False, output_type='div')
        context['bar_div'] = bar_div

        return context

class ShowPersonalProfileView(LoginRequiredMixin, DetailView):
    '''
    A view to show the personal profile of the logged in user
    '''
    model = Profile
    template_name = 'project/show_profile.html'

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ''' Add additional context like a graph of ratings to the view '''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        # get all items that the user is selling
        user = self.request.user
        profile = Profile.objects.get(user=user)
        items = Item.objects.filter(seller=profile)
        sold_items = items.filter(is_sold=True).order_by('-timestamp')
        sale_items = items.filter(is_sold=False).order_by('-timestamp')
        # calculate total revenue
        total_revenue = sum([item.price for item in sold_items])
        context['total_revenue'] = total_revenue

        context['sold_items'] = sold_items
        context['sale_items'] = sale_items

        # gather all ratings
        reviews = profile.review_set.all()
        ratings = [review.rating for review in reviews]

        # count the number of each rating
        rating_counts = defaultdict(int)
        for rating in ratings:
            rating_counts[rating] += 1
        
        # fill in any missing ratings
        for i in range(6):
            if i not in rating_counts:
                rating_counts[i] = 0
        
        # create a bar graph of the ratings
        y = list(range(6))
        x = [rating_counts[rating] for rating in y]
        
        # create the plotly figure
        fig = go.Figure(go.Bar(x=x, y=y, orientation='h'))

        # update the layout
        fig.update_layout(
            width=400,
            height=300,
            title="Seller Ratings",
            xaxis_title="Count",
            yaxis_title="Rating",
            yaxis=dict(
                tickmode='array',
                tickvals=y,
                ticktext=[str(i) for i in y],
            )
        )
        # convert the plotly figure to a div and add to context
        bar_div = plotly.offline.plot({'data': fig.data, 'layout': fig.layout}, auto_open=False, output_type='div')
        context['bar_div'] = bar_div

        return context

class CreatePostingView(LoginRequiredMixin, CreateView):
    ''' A view to create a new item and save to db '''
    form_class = CreateItemForm
    template_name = 'project/create_posting.html'
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        '''Handle submmission, needs to set foreign key'''
        user = self.request.user
        profile = Profile.objects.get(user=user)
        # set the seller to the current user
        form.instance.seller = profile
        # save the item
        item = form.save()
        # save the images
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
            # save the user
            user = user_form.save()
            profile = form.save(commit=False)
            profile.user = user
            # save the profile
            profile.save()
            print(profile)
            login(self.request, user)
            return redirect(reverse('profile'))
        else:
            return render(self.request, self.template_name, {'form': form, 'user_form': user_form})

    def get_success_url(self):
        return reverse('show_all_users')
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    ''' A view to update a profile '''
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
    ''' A view to update a listing '''
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
        # delete all images
        item.image_set.all().delete()
        # save the images
        files = self.request.FILES.getlist('files')
        for f in files:
            Image.objects.create(image_file=f, item=item)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_item', kwargs={'pk': self.object.pk})

class DeleteListingView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """A view to delete a status message"""
    model = Item
    template_name = 'project/delete_listing.html'
    context_object_name = 'item'

    def get_success_url(self) -> str:
        return reverse('profile')
    
    def test_func(self) -> bool | None:
        item = self.get_object()
        return item.seller.user == self.request.user

    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'project/no_permission.html', {
            'message': "You are not authorized to edit this listing."
        })
    
class PurchaseConfirmationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    ''' A view to confirm a purchase '''
    model = Item
    template_name = 'project/purchase_confirmation.html'
    context_object_name = 'item'
    fields = ['is_sold', 'buyer', 'sold_timestamp']

    def test_func(self) -> bool | None:
        item = self.get_object()
        print(item.seller.user)
        print(self.request.user)
        return item.seller.user != self.request.user
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'project/no_permission.html', {
            'message': "You cannot purchase your own item."
        })

    def get_success_url(self) -> str:
        return reverse('show_item', kwargs={'pk': self.object.pk})
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        print("form is invalid")
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        context['timestamp'] = datetime.datetime.now()  # Pass the current timestamp
        return context


class ShowPurchaseHistoryView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'project/purchase_history.html'
    context_object_name = 'items'

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        items = Item.objects.filter(buyer=profile).order_by('-timestamp')
        return items

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        total_spent = sum([item.price for item in context['items']])
        context['total_spent'] = total_spent
        return context 


class CreateReviewView(LoginRequiredMixin, CreateView):
    ''' A view to create a new review and save to db '''
    model = Item
    form_class = CreateReviewForm
    template_name = 'project/create_review.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        item = self.get_object()
        # use the form to create and save a review
        form.instance.reviewer = Profile.objects.get(user=self.request.user)
        form.instance.seller = item.seller
        form.instance.item = item
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        context['item'] = item
        return context

    def get_success_url(self) -> str:
        return reverse('show_item', kwargs={'pk': self.object.item.pk})

class UpdateReviewView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    ''' A view to update a review '''
    model = Review
    form_class = UpdateReviewForm
    template_name = 'project/update_review.html'

    def test_func(self) -> bool | None:
        review = self.get_object()
        return review.reviewer.user == self.request.user

    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'project/no_permission.html', {
            'message': "You are not authorized to edit this review."
        })

    def get_success_url(self) -> str:
        return reverse('show_item', kwargs={'pk': self.object.item.pk})
class DeleteReviewView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    ''' A view to delete a review '''
    model = Review
    template_name = 'project/delete_review.html'
    context_object_name = 'review'

    def test_func(self) -> bool | None:
        review = self.get_object()
        return review.reviewer.user == self.request.user

    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'project/no_permission.html', {
            'message': "You are not authorized to delete this review."
        })

    def get_success_url(self) -> str:
        return reverse('show_item', kwargs={'pk': self.object.item.pk})
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['item'] = self.get_object().item
        return context


