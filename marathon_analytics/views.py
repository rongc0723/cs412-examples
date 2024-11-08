from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Result

import plotly
import plotly.graph_objs as go# Create your views here.

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

class ResultDetailView(DetailView):
    '''Display a single result'''
    template_name = 'marathon_analytics/result_detail.html'
    model = Result
    context_object_name = 'r'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # get superclass version of context
        context = super().get_context_data(**kwargs)
        r = context['r'] # obtain the single Result instance
        # get data: half marathon splits
        first_half_seconds = r.time_half1.hour*3600 + r.time_half1.minute*60 + r.time_half1.second
        second_half_seconds = r.time_half2.hour*3600 + r.time_half2.minute*60 + r.time_half2.second

        # build a pie chart
        x = ['first half time', 'second half time']
        y = [first_half_seconds, second_half_seconds]
        print(f'x={x}')
        print(f'y={y}')
        fig = go.Pie(labels=x, values=y)
        pie_div = plotly.offline.plot({'data': [fig]}, auto_open=False, output_type='div')

        # add the piechart to context
        context['pie_div'] = pie_div

        #create bar chart with number of runners passed and who passed by
        x = [f'runners passed by {r.first_name}', f'runners who passed {r.first_name}']
        y = [r.get_runners_passed(), r.get_runners_passed_by()]
        fig = go.Bar(x=x, y=y)
        bar_div = plotly.offline.plot({'data': [fig]}, auto_open=False, output_type='div')
        context['bar_div'] = bar_div

        return context
