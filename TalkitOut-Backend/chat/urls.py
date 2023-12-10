from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('edit/<str:msg_id>/', views.edit_chat, name='edit_msg'),
    path('edit/delete/<str:msg_id>', views.delete_chat, name='delete_chat'),
    path('link/<str:msg_id>/', views.link, name='redirect_out'),
    path('new/meeting/',views.videocall, name='meeting'),
    path('new/join/',views.join_room, name='join_room'),
    path('export_chat/<str:room_name>/', views.export_chat, name='export_chat'),
]