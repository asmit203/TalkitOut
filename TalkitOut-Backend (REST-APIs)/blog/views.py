from re import template
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import post, announcements, Friend, Group, Comment
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.models import User
from .forms import announcement_form, CreateGroupForm
from users.models import Profile
from django.utils import timezone


def home(request):
    context = {
        "posts": post.objects.all(),
    }
    if request.user.is_authenticated:
        request.user.profile.lastseen = timezone.now()
        request.user.profile.save()
        current_user = request.user
        friends = Friend.objects.filter(user=current_user).values_list(
            "friend", flat=True
        )
        others = User.objects.exclude(pk=current_user.id).exclude(pk__in=friends)
        groups = Group.objects.filter(
            members=current_user
        )  # Get groups the user is a part of
        context["friends"] = Friend.objects.filter(user=current_user)
        context["others_list"] = others
        context["groups"] = groups  # Add groups to the context
        friends_lastseen = Profile.objects.filter(
            user__in=friends.values_list("friend", flat=True)
        ).values("user__username", "lastseen")
        context["friends_lastseen"] = friends_lastseen
    print(context)

    return render(request, "blog/home.html", context)


def add_friend(request, username):
    request.user.profile.lastseen = timezone.now()
    request.user.profile.save()
    if request.user.is_authenticated:
        current_user = request.user
        new_friend = User.objects.get(username=username)
        Friend.make_friendship(current_user, new_friend)
        room_name = (
            min(current_user.username, new_friend.username)
            + "_"
            + max(current_user.username, new_friend.username)
        )
        return redirect("room", room_name=room_name)


# class PostListViews(ListView):
#     model = post
#     template_name = 'blog/home.html'
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#     paginate_by = 5


class UserPostListViews(ListView):
    model = post
    template_name = "blog/User_posts.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5

    # <app>/<model>_<viewtype>.html
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return post.objects.filter(author=user).order_by("-date_posted")


class PostDetailsView(DetailView):
    model = post

    # template_name = 'blog/your_template_name.html'
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        post_instance = get_object_or_404(post, id=self.kwargs["pk"])

        votes_connected = get_object_or_404(post, id=self.kwargs["pk"])
        voted = False
        if votes_connected.votes.filter(id=self.request.user.id).exists():
            voted = True
        data["number_of_votes"] = votes_connected.number_of_votes()
        data["post_is_voted"] = voted

        # Commenting logic
        comments = post_instance.comments.all()
        data["comments"] = comments
        return data


def PostVote(request, pk):
    Post = get_object_or_404(post, id=request.POST.get("post_id"))
    if Post.votes.filter(id=request.user.id).exists():
        Post.votes.remove(request.user)
    else:
        Post.votes.add(request.user)
    return HttpResponseRedirect(reverse("post-detail", args=[str(pk)]))


class CommentCreateView(CreateView):
    model = Comment
    template_name = "blog/comment_form.html"  # Create a comment form template
    fields = ["text"]

    def form_valid(self, form):
        form.instance.post = get_object_or_404(post, id=self.kwargs["pk"])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", args=[str(self.kwargs["pk"])])


class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, DeleteView
):  # left of anything will be mixins
    model = post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    request.user.profile.lastseen = timezone.now()
    request.user.profile.save()
    context = {"title": "about"}
    if request.user.is_authenticated:
        request.user.profile.lastseen = timezone.now()
        request.user.profile.save()
        current_user = request.user
        friends = Friend.objects.filter(user=current_user).values_list(
            "friend", flat=True
        )
        others = User.objects.exclude(pk=current_user.id).exclude(pk__in=friends)
        groups = Group.objects.filter(
            members=current_user
        )  # Get groups the user is a part of
        context["friends"] = Friend.objects.filter(user=current_user)
        context["others_list"] = others
        context["groups"] = groups  # Add groups to the context
        friends_lastseen = Profile.objects.filter(
            user__in=friends.values_list("friend", flat=True)
        ).values("user__username", "lastseen")
        context["friends_lastseen"] = friends_lastseen
    return render(request, "blog/about.html", context)


class UpVotedPostListViews(ListView):
    model = post
    template_name = "blog/upvotedposts.html"
    context_object_name = "posts"
    ordering = ["-votes"]
    paginate_by = 5


def favourite_add(request, id):
    request.user.profile.lastseen = timezone.now()
    request.user.profile.save()
    Post = get_object_or_404(post, id=id)
    if Post.favourites.filter(id=request.user.id).exists():
        Post.favourites.remove(request.user)

    else:
        Post.favourites.add(request.user)

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def favourite_list(request):
    request.user.profile.lastseen = timezone.now()
    request.user.profile.save()
    new = post.objects.filter(favourites=request.user)
    context = {"new": new}
    if request.user.is_authenticated:
        request.user.profile.lastseen = timezone.now()
        request.user.profile.save()
        current_user = request.user
        friends = Friend.objects.filter(user=current_user).values_list(
            "friend", flat=True
        )
        others = User.objects.exclude(pk=current_user.id).exclude(pk__in=friends)
        groups = Group.objects.filter(
            members=current_user
        )  # Get groups the user is a part of
        context["friends"] = Friend.objects.filter(user=current_user)
        context["others_list"] = others
        context["groups"] = groups  # Add groups to the context
        friends_lastseen = Profile.objects.filter(
            user__in=friends.values_list("friend", flat=True)
        ).values("user__username", "lastseen")
        context["friends_lastseen"] = friends_lastseen
    return render(request, "blog/favourites.html", context)


def Announce(request):
    request.user.profile.lastseen = timezone.now()
    request.user.profile.save()
    form = announcement_form()

    allAnnouncements = announcements.objects.all()

    user_detail = request.user
    context = {
        "announcements": allAnnouncements,
        "user_detail": user_detail,
        "form": form,
    }

    if request.method == "POST":
        # title=request.POST['title']
        # announces=request.POST['announce']
        # announcements.objects.create(title=title,announce=announces)
        # allAnnouncements=announcements.objects.all()

        # user_detail = request.user
        # context={'announcements':allAnnouncements,'user_detail':user_detail,'form':form}
        form = announcement_form(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "blog/announcement.html", context)
    return render(request, "blog/announcement.html", context)


def create_group_page(request):
    request.user.profile.lastseen = timezone.now()
    request.user.profile.save()
    current_user = request.user

    context = {"users": User.objects.exclude(pk=current_user.id)}
    if request.user.is_authenticated:
        request.user.profile.lastseen = timezone.now()
        request.user.profile.save()
        friends = Friend.objects.filter(user=current_user).values_list(
            "friend", flat=True
        )
        others = User.objects.exclude(pk=current_user.id).exclude(pk__in=friends)
        groups = Group.objects.filter(
            members=current_user
        )  # Get groups the user is a part of
        context["friends"] = Friend.objects.filter(user=current_user)
        context["others_list"] = others
        context["groups"] = groups  # Add groups to the context
        friends_lastseen = Profile.objects.filter(
            user__in=friends.values_list("friend", flat=True)
        ).values("user__username", "lastseen")
        context["friends_lastseen"] = friends_lastseen
    print(context)
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data["group_name"]
            members = list(form.cleaned_data["members"])
            members.append(current_user)
            # Create the group
            new_group = Group.objects.create(name=group_name)
            new_group.members.set(members)

            return redirect("blog-home")
    else:
        form = CreateGroupForm()

    context["form"] = form
    return render(request, "blog/create_group.html", context)
