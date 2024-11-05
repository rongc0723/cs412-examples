from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from .models import Result

# Create your views here.
class ResultsListView(ListView):
    '''A view to show all results.'''
    template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = 'results'
    paginate_by = 50

    def get_queryset(self) -> QuerySet[Any]:
        '''return the set of results'''
        qs = super().get_queryset()
        if 'City' in self.request.GET:
            qs = qs.filter(city=self.request.GET['City'])
        return qs # return 25 for now

