from django.urls import path
from .views import PostListViews,PostDetailsView
from . import views
urlpatterns = [
    path('', PostListViews.as_view(),name='blog-home'),
    path('post/<int:pk>/', PostDetailsView.as_view(),name='post-detail'),
    path('about/', views.about,name='blog-about'),
]