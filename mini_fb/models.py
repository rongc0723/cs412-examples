from django.db import models
from django.urls import reverse
# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    city = models.CharField(max_length=30, blank=True)
    email_address = models.EmailField(blank=False)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_status_messages(self):
        '''Return all status messages for this profile and order by timestamp'''
        status_messages = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
        return status_messages
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})


class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.message} by {self.profile.name} at {self.timestamp}'