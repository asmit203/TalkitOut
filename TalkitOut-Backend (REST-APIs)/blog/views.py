from re import template
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import post, announcements, Friend, Group, Comment
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.models import User
from .forms import announcement_form, CreateGroupForm
from users.models import Profile
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import (
    PostSerializer,
    UserSerializer,
    FriendSerializer,
    LastSeenSerializer,
    UserNotFriendSerializer,
    GroupSerializer,
    AnnouncementSerializer,
)
from django.contrib.auth.decorators import login_required
import json
from rest_framework.generics import RetrieveAPIView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
import hashlib, base64
import urllib.parse


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


def redirect_custom(request, **kwargs):
    return HttpResponseRedirect("http://localhost:%s" % kwargs.get("port"))


@api_view(["GET"])
def home_posts(request):
    posts = post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@login_required
def friends(request):
    current_user = request.user
    friends = Friend.objects.filter(user=current_user)

    serializer = FriendSerializer(friends, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@login_required
def get_friends_last_seen(request):
    current_user = request.user
    friends = Friend.objects.filter(user=current_user)

    friend_usernames = friends.values_list("friend__username", flat=True)
    friends_lastseen = Profile.objects.filter(
        user__username__in=friend_usernames
    ).values("user__username", "lastseen")

    serializer = LastSeenSerializer(friends_lastseen, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@login_required
def get_users_not_friends(request):
    current_user = request.user
    friends = Friend.objects.filter(user=current_user)

    users_not_friends = User.objects.exclude(pk=current_user.id).exclude(
        pk__in=friends.values_list("friend", flat=True)
    )

    serializer = UserNotFriendSerializer(users_not_friends, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@login_required
def get_user_groups(request):
    current_user = request.user
    user_groups = Group.objects.filter(members=current_user)

    serializer = GroupSerializer(user_groups, many=True)

    return Response(serializer.data)


def user(request):
    return HttpResponse(
        json.dumps(
            {
                "username": request.user.username,
                "email": request.user.email,
                "is_superuser": request.user.is_superuser,
            }
        )
    )


def is_authenticated(request):
    return HttpResponse(json.dumps(request.user.is_authenticated))


def getHash(s):
    s_norm = s.lower().strip()
    return hashlib.sha256(s_norm.encode("utf-8")).hexdigest()


def add_friend(request, username):
    request.user.profile.lastseen = timezone.now()
    request.user.profile.save()
    if request.user.is_authenticated:
        current_user = request.user
        new_friend = User.objects.get(username=username)
        Friend.make_friendship(current_user, new_friend)
        room_name = getHash(
            min(current_user.email, new_friend.email)
            + "_"
            + max(new_friend.email, current_user.email)
        )
        return redirect("room", room_name=room_name)


# class PostListViews(ListView):
#     model = post
#     template_name = 'blog/home.html'
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#     paginate_by = 5


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5  # Adjust the page size as needed


class UserPostListView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return post.objects.filter(author=user).order_by("-date_posted")


class PostDetailsAPIView(RetrieveAPIView):
    queryset = post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        # Voting logic
        voted = instance.votes.filter(id=self.request.user.id).exists()
        number_of_votes = instance.number_of_votes()

        # Commenting logic
        comments = instance.comments.all()
        # Serialize the User object
        author_data = UserSerializer(instance.author).data

        data = {
            "post": PostSerializer(instance).data,
            "author": author_data,
            "number_of_votes": number_of_votes,
            "post_is_voted": voted,
            "comments": [
                {"author": comment.author.username, "text": comment.text}
                for comment in comments
            ],
        }
        return JsonResponse(data)


# @csrf_exempt
def PostVote(request, pk):
    Post = get_object_or_404(post, id=request.POST.get("post_id"))
    print(request.POST.get("post_id"), Post)
    if Post.votes.filter(id=request.user.id).exists():
        Post.votes.remove(request.user)
    else:
        Post.votes.add(request.user)
    return JsonResponse({"redirect_url": "/post/" + str(pk)})


class CommentCreateView(CreateView):
    model = Comment
    template_name = "blog/comment_form.html"  # Create a comment form template
    fields = ["text"]

    def form_valid(self, form):
        print(form)
        form.instance.post = get_object_or_404(post, id=self.kwargs["pk"])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return JsonResponse({"redirect_url": "/post/" + self.kwargs["pk"]})


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


class PostDeleteAPIView(DestroyAPIView):
    queryset = post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post = self.get_object()

        # Check if the user has permission to delete the post
        if request.user == post.author:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"detail": "You do not have permission to delete this post."},
                status=status.HTTP_403_FORBIDDEN,
            )


def about(request):
    
    context = {"title": "about"}
    if request.user.is_authenticated:
        request.user.profile.lastseen = timezone.now()
        request.user.profile.save()
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


class UpVotedPostListViews(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return post.objects.annotate(num_votes=Count("votes")).order_by(
            "-num_votes", "id"
        )


@require_POST
def favourite_add(request, id):
    request.user.profile.lastseen = timezone.now()
    request.user.profile.save()

    post_obj = get_object_or_404(post, id=id)

    if post_obj.favourites.filter(id=request.user.id).exists():
        post_obj.favourites.remove(request.user)
    else:
        post_obj.favourites.add(request.user)

    return JsonResponse({"status": "success"})


@api_view(["GET"])
def favourite_list(request):
    posts = post.objects.filter(favourites=request.user)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


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



# @csrf_exempt
@api_view(["GET", "POST"])
def announce_list(request):
    request.user.profile.lastseen = timezone.now()
    request.user.profile.save()

    if request.method == "GET":
        all_announcements = announcements.objects.all()
        serializer = AnnouncementSerializer(all_announcements, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        form = announcement_form(request.data)
        if form.is_valid():
            form.save()
            return Response(status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


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

            return HttpResponseRedirect("http://localhost:3000/")
    else:
        form = CreateGroupForm()

    context["form"] = form
    return render(request, "blog/create_group.html", context)


def current_user(request):
    print(User.objects.get(username=request.user.username))
    return HttpResponse(request.user)
