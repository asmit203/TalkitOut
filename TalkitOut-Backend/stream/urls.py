from . import views
from . views import (
    VideoDetailView, 
    UserVideoListView, 
    VideoCreateView, 
    GeneralVideoListView, 
    VideoUpdateView,
    VideoDeleteView,
)
from django.urls import path 


app_name = "stream"

urlpatterns = [
    # path('user/<str:username>',UserVideoListView.as_view(),name="video-list"),
    path('',GeneralVideoListView.as_view(), name="video-list"),
    path('file/<int:pk>/', VideoDetailView.as_view(), name="video-detail"),
    path('file/<int:pk>/update/', VideoUpdateView.as_view(), name="video-update"),
    path('file/<int:pk>/delete/', VideoDeleteView.as_view(), name="video-delete"),
    path('user/<str:username>', UserVideoListView.as_view(), name="user-videos"),
    path('file/new/',VideoCreateView.as_view(), name="video-create"),
    path('search',views.search,name="search"),
]