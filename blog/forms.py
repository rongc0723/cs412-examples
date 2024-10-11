from django import forms
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    '''A form to add a comment to the database'''

    class Meta:
        '''Associate this form with the Comment model; select fields'''
        model = Comment
        fields = ['author', 'text']