from rest_framework import permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(ModelViewSet):
    """ ViewSet for viewing and editing user """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        """ Return permissions based on action """
        if self.action in ['create']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
