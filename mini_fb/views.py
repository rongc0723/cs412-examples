from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render
from .models import Profile
from .forms import CreateProfileForm
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

    def get_success_url(self) -> str:
        return reverse('show_profile', kwargs={'pk': self.object.pk})
