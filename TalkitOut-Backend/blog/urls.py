from django.urls import path, include

from .views import (
    # PostListViews,
    PostDetailsView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListViews,
    UpVotedPostListViews,
    PostVote,
    CommentCreateView,
    home,
    add_friend
)
from stream.views import *
from chat import views
from . import views

urlpatterns = [
    path('', home, name='blog-home'),
    path('user/<str:username>', UserPostListViews.as_view(),name='user-posts'),
    path('post/<int:pk>/', PostDetailsView.as_view(),name='post-detail'),
    path('post/new/', PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(),name='post-delete'),
    path('about/', views.about,name='blog-about'),
    path('upvoted/',UpVotedPostListViews.as_view(),name='upvoted-posts'),
    path('post-vote/<int:pk>', views.PostVote, name="post_vote"),
    path('post/comment/<int:pk>/', CommentCreateView.as_view(), name='add-comment'),
    path('fav/<int:id>/',views.favourite_add,name='favourite_add'),
    path('favourites/',views.favourite_list,name='favourite_list'),
    path('announcements/',views.Announce,name='announce'),
    path('stream/',GeneralVideoListView.as_view(),name='stream'),
    # path('stream/', include('stream.urls')),
    path('chat/', include('chat.urls')),
    path('add_friend/<str:username>/', views.add_friend, name='add_friend'),
    path('create_group/', views.create_group_page, name='create_group'),
]