# permission_server/core/serializers.py
from rest_framework import serializers
from .models import CustomUser, Role

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'department']
        read_only_fields = ['id']