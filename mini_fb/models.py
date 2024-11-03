from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    """Model for a user profile"""
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    city = models.CharField(max_length=30, blank=True)
    email_address = models.EmailField(blank=False)
    profile_image_url = models.URLField(blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_status_messages(self):
        '''Return all status messages for this profile and order by timestamp'''
        status_messages = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
        return status_messages

    def get_friends(self):
        '''Return all friends for this profile in a list'''
        friends = []
        friend_relations = Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)
        for relation in friend_relations:
            if relation.profile1 == self:
                friends.append(relation.profile2)
            else:
                friends.append(relation.profile1)
        return friends

    def add_friend(self, friend):
        '''Add a friend to this profile'''
        # check if friendship exists
        friend_relations = Friend.objects.filter(profile1=self, profile2=friend) | Friend.objects.filter(profile1=friend, profile2=self)
        if self != friend and len(friend_relations) == 0:
            friend_relation = Friend(profile1=self, profile2=friend)
            friend_relation.save()

    def get_friend_suggestions(self):
        ''' Return list or queryset of possible friends for a profile'''
        # get all friends
        friends = self.get_friends()
        # get all profiles except friends and self
        all_profiles = Profile.objects.exclude(pk=self.pk)
        friend_pks = [f.pk for f in friends]
        suggestions = all_profiles.exclude(pk__in=friend_pks)
        return suggestions
    
    def get_news_feed(self):
        '''Return status messages for each of the friends of a given user 
        and themself, most recent at top'''
        friends = self.get_friends()
        # get all statu messages of friends and self
        all_status_messages = StatusMessage.objects.filter(profile=self) | StatusMessage.objects.filter(profile__in=friends)
        # order by timestamp
        all_status_messages = all_status_messages.order_by('-timestamp')
        return all_status_messages

    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})

class Friend(models.Model):
    """Model for a friend relationship"""
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile1} & {self.profile2}'


class StatusMessage(models.Model):
    """Model for a status message"""
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def get_images(self):
        '''Return all images for this status message'''
        images = Image.objects.filter(status_message=self)
        return images

    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.profile.pk})
    
    def __str__(self):
        return f'{self.message} by {self.profile.first_name} at {self.timestamp}'

class Image(models.Model):
    """Model for an image"""
    image_file = models.ImageField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.image_file}'