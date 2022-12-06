from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

class post(models.Model):
    title = models.CharField(max_length=100)
    # content = models.TextField()
    content = RichTextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    votes=models.ManyToManyField(User,related_name='post_vote')

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
    def number_of_votes(self):
        return self.votes.count()
class announcements(models.Model):
    title=models.CharField(max_length=50,default="TITLE")
    announce=models.TextField(max_length=200)
    def __str__(self):
        return self.title
