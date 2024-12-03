from django.urls import path
from .views import chatbotResponse

urlpatterns = [
    path("", chatbotResponse, name="index"),
]
