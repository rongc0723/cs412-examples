from django import forms
from .models import Item, Profile

class CreateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'type_of_item', 'description', 'price']

class CreateProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=True)
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'email_address', 'profile_picture']

class UpdateListingForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'type_of_item', 'description', 'price']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'city', 'email_address', 'phone_number', 'profile_picture']