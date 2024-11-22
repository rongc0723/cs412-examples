from django import forms
from .models import Item

class CreateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'type_of_item', 'description', 'price']
        