## project/forms.py
## descrption: the forms for the project application
from django import forms
from .models import Item, Profile, Review

class CreateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'type_of_item', 'description', 'price']
        labels = {
            'item_name': 'Item name',
            'type_of_item': 'Type of item',
            'description': 'Leave a comment about your item',
            'price': 'Price',
        }

class CreateProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=True)
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'email_address', 'profile_picture']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email_address': 'Email address',
            'profile_picture': 'Profile picture',
        }
class UpdateListingForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'type_of_item', 'description', 'price']
        labels = {
            'item_name': 'Item name',
            'type_of_item': 'Type of item',
            'description': 'Leave a comment about your item',
            'price': 'Price',
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'city', 'email_address', 'phone_number', 'profile_picture']
    
class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']

class UpdateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        labels = {
            'rating': 'Rate (1-5)',
            'review_text': 'Leave a comment',
        }