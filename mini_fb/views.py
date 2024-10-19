from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.urls import reverse
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

class CreateProfileView(CreateView):
    ''' A view to create a new profile and save to db'''
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    
class CreateStatusMessageView(CreateView):
    ''' A view to create a new status message and save to db'''
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        '''Handle submmission, needs to set foreign key'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        sm = form.save()
        files = self.request.FILES.getlist('files')
        for f in files:
            Image.objects.create(image_file=f, status_message=sm)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''build dict of context data for the view'''
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

class UpdateProfileView(UpdateView):
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    model = Profile

class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self) -> str:
        return reverse('show_profile', kwargs={'pk': self.get_object().profile.pk})
    
class UpdateStatusMessageView(UpdateView):
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    model = StatusMessage
    context_object_name = 'status_message'

