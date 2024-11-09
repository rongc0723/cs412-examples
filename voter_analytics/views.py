from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Voter

# Create your views here.

class VotersListView(ListView):
    '''A view to show all voters.'''
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct().order_by('voter_score')
        # Get min and max year
        min_year = Voter.objects.order_by('year_of_birth').values_list('year_of_birth', flat=True).first()
        max_year = Voter.objects.order_by('-year_of_birth').values_list('year_of_birth', flat=True).first()
        context['year_range'] = range(min_year, max_year+1)
        context['min_year'] = min_year
        context['max_year'] = max_year
        context['voted_in_election'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        return context

    def get_queryset(self):
        '''return voters based on filter'''
        qs = super().get_queryset()
        party_affiliation = self.request.GET.get('party_affiliation')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        voter_score = self.request.GET.get('voter_score')
        voted_in_election = self.request.GET.getlist('voted_in_election')
        if party_affiliation:
            qs = qs.filter(party_affiliation=party_affiliation)
        if voter_score:
            qs = qs.filter(voter_score=voter_score)
        if voted_in_election:
            for election in voted_in_election:
                if election == 'v20state':
                    qs = qs.filter(v20state='TRUE')
                if election == 'v21town':
                    qs = qs.filter(v21town='TRUE')
                if election == 'v21primary':
                    qs = qs.filter(v21primary='TRUE')
                if election == 'v22general':
                    qs = qs.filter(v22general='TRUE')
                if election == 'v23town':
                    qs = qs.filter(v23town='TRUE')
        if min_year:
            qs = qs.filter(year_of_birth__gte=min_year)
        if max_year:
            qs = qs.filter(year_of_birth__lte=max_year)
        return qs

class VoterDetailView(DetailView):
    '''Display a single voter'''
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'
