from django.db import models

# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    name  = models.TextField(blank=False)
    city = models.CharField(max_length=30, blank=True)
    email_address = models.EmailField(blank=False)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name