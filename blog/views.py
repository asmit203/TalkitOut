from re import template
from django.shortcuts import render
from django.http import HttpResponse
from .models import post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
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
class PostDetailsView(DetailView):
    model = post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = post
    fields = ['title','content']
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = post
    fields = ['title','content']
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):  #left of anything will be mixins
    model = post
    success_url = "/"
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False
def about(request):
    return render(request, 'blog/about.html',{'title':'about'})
