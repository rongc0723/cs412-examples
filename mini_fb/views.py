from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import render
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class ShowAllView(ListView):
    model = Profile

    context_object_name = 'profiles'

    template_name = 'mini_fb/show_all_profiles.html'

class ShowProfilePageView(DetailView):
    ''' Show the details for one profile'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class ShowPersonalProfileView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

class CreateProfileView(CreateView):
    ''' A view to create a new profile and save to db'''
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    ''' A view to create a new status message and save to db'''
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'


    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        '''Handle submmission, needs to set foreign key'''
        user = self.request.user
        profile = Profile.objects.get(user=user)
        form.instance.profile = profile
        sm = form.save()
        files = self.request.FILES.getlist('files')
        for f in files:
            Image.objects.create(image_file=f, status_message=sm)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''build dict of context data for the view'''
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.get(user=user)
        pk = profile.pk
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """A view to update a profile"""
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    model = Profile
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    """A view to delete a status message"""
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self) -> str:
        return reverse('show_profile', kwargs={'pk': self.get_object().profile.pk})
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    """A view to update a status message"""
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    model = StatusMessage
    context_object_name = 'status_message'

class CreateFriendView(LoginRequiredMixin, View):
    """A view to create a friend relationship"""
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user = self.request.user
        profile = Profile.objects.get(user=user)
        if request.method == 'GET':
            other_profile = Profile.objects.get(pk=kwargs['other_pk'])
            profile.add_friend(other_profile)
            return redirect(reverse('show_profile', kwargs={'pk': profile.pk}))

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    ''' Show friend suggestions for a profile'''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile


class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    ''' Show news feed for a profile'''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile