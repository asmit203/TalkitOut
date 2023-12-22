from django.core import serializers
from rest_framework import serializers
from .models import post, Friend, Group, announcements
from users.models import Profile
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["image"]  # Add more profile fields as needed


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile"]  # Add more fields as needed


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    votes = UserSerializer(many=True)
    favourites = UserSerializer(many=True)

    class Meta:
        model = post
        fields = [
            "id",
            "title",
            "content",
            "date_posted",
            "author",
            "votes",
            "favourites",
        ]


class FriendSerializer(serializers.ModelSerializer):
    friend = UserSerializer()

    class Meta:
        model = Friend
        fields = ["id", "user", "friend"]


class LastSeenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user__username"
    )  # Use source to match the key in the queryset

    class Meta:
        model = Profile
        fields = ["username", "lastseen"]


class UserNotFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]  # Add more fields as needed


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = announcements
        fields = ["id", "title", "description"]
