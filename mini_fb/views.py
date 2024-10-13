from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Profile
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