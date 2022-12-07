from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from PIL import Image

# Create your models here.

class post(models.Model):
    title = models.CharField(max_length=100)
    # content = models.TextField()
    content = RichTextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    votes=models.ManyToManyField(User,related_name='post_vote')
    image=models.ImageField(default='',upload_to='photos',blank=True)
    favourites=models.ManyToManyField(User,related_name="favourite",default=None,blank=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
    def number_of_votes(self):
        return self.votes.count()


class announcements(models.Model):
    title=models.CharField(max_length=50,default="TITLE")
    description= RichTextField()

    def __str__(self):
        return self.title