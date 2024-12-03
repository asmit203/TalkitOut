from django.urls import path
from . import views

urlpatterns = [
    path('verify-permission/', views.verify_permission, name='verify_permission'),
]
