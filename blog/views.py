from re import template
from django.shortcuts import render
from django.http import HttpResponse
from .models import post
from django.views.generic import ListView,DetailView
# Create your views here.
# posts = [{
#     'author': 'asmit',
#     'title': '01',
#     'content': '1st comment',
#     'date_posted': '02/04/2022',
# },
#     {
#         'author': 'abhraneel',
#         'title': '02',
#         'content': '2nd comment',
#         'date_posted': '03/04/2022',
# },
#     {
#         'author': 'aritra',
#         'title': '03',
#         'content': '3rd comment',
#         'date_posted': '04/04/2022'
# }]


def home(request):
    context = {
        'posts' : post.objects.all()
    }
    return render(request, 'blog/home.html',context)

class PostListViews(ListView):
    model = post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    #<app>/<model>_<viewtype>.html
class PostDetailViews(ListView):
    model = post
    


def about(request):
    return render(request, 'blog/about.html',{'title':'about'})
