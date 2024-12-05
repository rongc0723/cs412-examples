from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Profile(models.Model):
    """Model for a profile of a user"""
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    username = models.CharField(max_length=30, blank=False)
    email_address = models.EmailField(blank=False)
    city = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    profile_picture = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_profile')

    def __str__(self):
        return self.username + ': ' + self.first_name + ' ' + self.last_name

    def get_ratings(self):
        reviews = Review.objects.filter(seller=self)
        ratings = [review.rating for review in reviews]
        if len(ratings) == 0:
            return 0
        return sum(ratings) / len(ratings)

class Item(models.Model):
    """Model for an item"""
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    item_name = models.CharField(max_length=30, blank=False)
    type_of_item = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    is_sold = models.BooleanField(default=False)
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='buyer', blank=True, null=True)

    def __str__(self):
        return f'{self.item_name} posting by {self.seller} posted on {self.timestamp.strftime("%m/%d/%Y, %H:%M:%S")}'

    def get_images(self):
        return Image.objects.filter(item=self)

    def get_review(self):
        return Review.objects.filter(item=self)

class Image(models.Model):
    """Model for an image"""
    image_file = models.ImageField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Image for {self.item}'

class Review(models.Model):
    """Model for a review"""
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviewer')
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False)
    review_text = models.TextField(blank=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.reviewer} rated {self.item} {self.rating} stars'