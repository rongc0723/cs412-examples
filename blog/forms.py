from django import forms
from .models import Comment
from .models import Article

class CreateCommentForm(forms.ModelForm):
    '''A form to add a comment to the database'''

    class Meta:
        '''Associate this form with the Comment model; select fields'''
        model = Comment
        fields = ['author', 'text']

class CreateArticleForm(forms.ModelForm):
    '''A form to add an article to the database'''

    class Meta:
        '''Associate this form with the Article model; select fields'''
        model = Article
        fields = ['title', 'author', 'text', 'image_file']

class UpdateArticleForm(forms.ModelForm):
    '''A form to update an article in the database'''

    class Meta:
        '''Associate this form with the Article model; select fields'''
        model = Article
        fields = ['title', 'text']