from django.urls import path, include

from .views import (
    # PostListViews,
    PostDetailsAPIView,
    PostCreateView,
    PostUpdateView,
    PostDeleteAPIView,
    UserPostListView,
    UpVotedPostListViews,
    PostVote,
    CommentCreateView,
    home_posts,
    add_friend,
    friends,
    get_friends_last_seen,
    get_users_not_friends,
    get_user_groups,
    PostVote,
)
from stream.views import *
from chat import views
from . import views

urlpatterns = [
    path("home_posts", home_posts, name="home_posts"),
    path("friends", friends, name="friends"),
    path("friends_last_seen", get_friends_last_seen, name="friends_last_seen"),
    path("others", get_users_not_friends, name="others"),
    path("groups", get_user_groups, name="groups"),
    path("is_authenticated/", views.is_authenticated, name="is_authenticated"),
    path("current_user/", views.user, name="current-user"),
    path("user/<str:username>", UserPostListView.as_view(), name="user-posts"),
    path("post/<int:pk>/", PostDetailsAPIView.as_view(), name="post-details-api"),
    path(
        "post-detail/<int:pk>/",
        lambda request, pk: redirect(f"http://localhost:3000/post/{pk}/"),
        name="post-detail",
    ),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteAPIView.as_view(), name="post-delete"),
    path("about/", views.about, name="blog-about"),
    path("upvoted/", UpVotedPostListViews.as_view(), name="upvoted-posts"),
    path("post-vote/<int:pk>/", PostVote, name="post_vote"),
    path("post/comment/<int:pk>/", CommentCreateView.as_view(), name="add-comment"),
    path("fav/<int:id>/", views.favourite_add, name="favourite_add"),
    path("favourites/", views.favourite_list, name="favourite_list"),
    path("announcements/", views.Announce, name="announce"),
    path("stream/", GeneralVideoListView.as_view(), name="stream"),
    # path('stream/', include('stream.urls')),
    path("chat/", include("chat.urls")),
    path("add_friend/<str:username>/", views.add_friend, name="add_friend"),
    path("create_group/", views.create_group_page, name="create_group"),
]
