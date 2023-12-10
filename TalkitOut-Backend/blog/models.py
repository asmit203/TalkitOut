from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

# class post(models.Model):
#     title = models.CharField(max_length=100)
#     # content = models.TextField()
#     content = RichTextField()
#     date_posted = models.DateTimeField(default=timezone.now)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     votes=models.ManyToManyField(User,related_name='post_vote')
#     favourites=models.ManyToManyField(User,related_name="favourite",default=None,blank=True)

#     def __str__(self):
#         return self.title
#     def get_absolute_url(self):
#         return reverse('post-detail',kwargs={'pk':self.pk})
#     def number_of_votes(self):
#         return self.votes.count()
    
class post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = models.ManyToManyField(User, related_name='post_vote')
    favourites = models.ManyToManyField(User, related_name="favourite", default=None, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def number_of_votes(self):
        return self.votes.count()
    
class Comment(models.Model):
    post = models.ForeignKey('post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class announcements(models.Model):
    title=models.CharField(max_length=50,default="TITLE")
    description= RichTextField()

    def __str__(self):
        return self.title
    
class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f'{self.user.username} - {self.friend.username}'

    @classmethod
    def make_friendship(cls, user, friend):
        # Creating the friendship in both directions
        cls.objects.get_or_create(user=user, friend=friend)
        cls.objects.get_or_create(user=friend, friend=user)
        
class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(User, related_name='group_members')

    def __str__(self):
        return self.name
    