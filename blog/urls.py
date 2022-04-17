from django.urls import path
from .views import PostListViews,PostDetailViews
from . import views
urlpatterns = [
    path('', PostListViews.as_view(),name='blog-home'),
    path('post/<int:pk>/', PostDetailViews.as_view(),name='post-detail'),
    path('about/', views.about,name='blog-about'),
]