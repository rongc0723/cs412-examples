from django import forms
from .models import Voter

class VoterFilterForm(forms.Form):

    party_afficiation = forms.ChoiceField(
        choices=[('D', 'Democrat'), ('R', 'Republican'), ('U', 'Unaffiliated')],
        required=False,
        label='Party Affiliation'
    )

    min_dob = forms.ChoiceField(
        choices=[(str(year), str(year)) for year in range(1924, 2006)],
        required=False,
        label='Min Date of Birth'
    )
    max_dob = forms.ChoiceField(
        choices=[(str(year), str(year)) for year in range(1924, 2006)],
        required=False,
        label='Max Date of Birth'
    )

    voter_score = forms.ChoiceField(
        choices=[(str(score), str(score)) for score in range(0, 5)],
        required=False,
        label='Voter Score'
    )

    voted_in_election = forms.MultipleChoiceField(
        choices=[
            ('v20state', 'Voted in 2020 State Election'),
            ('v21town', 'Voted in 2021 Town Election'),
            ('v21primary', 'Voted in 2021 Primary Election'),
            ('v22general', 'Voted in 2022 General Election'),
            ('v23town', 'Voted in 2023 Town Election'),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Elections Voted"
    )

