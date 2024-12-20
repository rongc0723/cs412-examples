from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):

    '''each Attribute will be associated with a User'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    # image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        return f'{self.title} by {self.author}'
    def get_comments(self):
        '''Return all comments for this article'''
        comments = Comment.objects.filter(article=self)
        return comments
    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})
    
class Comment(models.Model):
    '''Encapsulate the idea of a comment on an article'''
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.text}'
    