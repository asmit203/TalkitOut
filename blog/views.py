from re import template
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import post,announcements
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
'''# Create your views here.
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
'''

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
    paginate_by = 5
class UserPostListViews(ListView):
    model = post
    template_name = 'blog/User_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    #<app>/<model>_<viewtype>.html
    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return post.objects.filter(author = user).order_by('-date_posted')

class PostDetailsView(DetailView):
    model = post

    def get_context_data(self,**kwargs):
        data = super().get_context_data(**kwargs)

        votes_connected = get_object_or_404(post, id=self.kwargs['pk'])
        voted = False
        if votes_connected.votes.filter(id=self.request.user.id).exists():
            voted = True
        data['number_of_votes'] = votes_connected.number_of_votes()
        data['post_is_voted'] = voted
        return data

def PostVote(request,pk):
    Post=get_object_or_404(post,id=request.POST.get('post_id'))
    if Post.votes.filter(id=request.user.id).exists():
        Post.votes.remove(request.user)
    else:
        Post.votes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))



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


class UpVotedPostListViews(ListView):
    model = post
    template_name = 'blog/upvotedposts.html'
    context_object_name = 'posts'
    ordering = ['-votes']
    paginate_by = 5


def favourite_add(request,id):
    Post=get_object_or_404(post,id=id)
    if Post.favourites.filter(id=request.user.id).exists():
        Post.favourites.remove(request.user)

    else:
        Post.favourites.add(request.user)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def favourite_list(request):
    new=post.objects.filter(favourites=request.user)
    return render(request,'blog/favourites.html',{'new':new})
def Announce(request):
    if request.method=='POST':
        title=request.POST['title']
        announces=request.POST['announce']
        announcements.objects.create(title=title,announce=announces)
    allAnnouncements=announcements.objects.all()
    
    user_detail = request.user
    context={'announcements':allAnnouncements,'user_detail':user_detail}
    return render(request,'blog/announcement.html',context)
