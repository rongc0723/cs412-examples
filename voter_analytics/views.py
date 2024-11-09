from typing import Any
from django.shortcuts import render
from django.views.generic import ListView

from .models import Voter
from .forms import VoterFilterForm

# Create your views here.

class VotersListView(ListView):
    '''A view to show all voters.'''
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm()
        return context

    # def get_queryset(self):
    #     '''return voters based on filter'''

    #     form = VoterFilterForm(self.request.GET)
    #     if form.is_valid():
    #         party_affiliation = form.cleaned_data['party_affiliation']
    #         min_dob = form.cleaned_data['min_dob']
    #         max_dob = form.cleaned_data['max_dob']
    #         voter_score = form.cleaned_data['voter_score']
    #         elections_voted = form.cleaned_data['elections_voted']

            

