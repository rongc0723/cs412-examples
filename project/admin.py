## project/admin.py
## descrption: the admin for the project application

from django.contrib import admin
from .models import Profile, Item, Review, Image
# Register your models here.

admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(Review)
admin.site.register(Image)

