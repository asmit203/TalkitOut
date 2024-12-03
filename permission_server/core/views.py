# permission_server/core/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CustomUser, Role
from .serializers import UserSerializer
from .permissions import IsAdminUser, IsManagerOrAdmin, ReadOnly, IsManager

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsManagerOrAdmin]
        elif self.action in ['create', 'destroy', 'update', 'partial_update']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [ReadOnly]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def change_role(self, request):
        username = request.data.get('username')
        new_role = request.data.get('role')
        
        try:
            user = CustomUser.objects.get(username=username)
            if new_role in dict(Role.choices):
                user.role = new_role
                user.save()
                return Response({
                    'message': f'Role changed for {username}', 
                    'new_role': new_role
                })
            else:
                return Response({
                    'error': 'Invalid role'
                }, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)