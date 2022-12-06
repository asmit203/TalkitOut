from django.urls import path
from .views import (
    PostListViews,
    PostDetailsView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListViews,
    UpVotedPostListViews,
    PostVote,
    Announce,

)
from . import views
urlpatterns = [
    path('', PostListViews.as_view(),name='blog-home'),
    path('user/<str:username>', UserPostListViews.as_view(),name='user-posts'),
    path('post/<int:pk>/', PostDetailsView.as_view(),name='post-detail'),
    path('post/new/', PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(),name='post-delete'),
    path('about/', views.about,name='blog-about'),
    path('upvoted/',UpVotedPostListViews.as_view(),name='upvoted-posts'),
    path('post-vote/<int:pk>', views.PostVote, name="post_vote"),
    path('announcements/',views.Announce,name='announce')

]