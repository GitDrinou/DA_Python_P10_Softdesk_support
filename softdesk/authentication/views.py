from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from .serializers import CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(ModelViewSet):
    """ ViewSet for viewing and editing user """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        """ Return permissions based on action """
        if self.action in ['create']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return User.objects.filter(is_staff=False)

    def get_object(self):
        obj = super().get_object()
        if obj != self.request.user:
            raise permissions.exceptions.PermissionDenied("You are note "
                                                          "authorized to "
                                                          "update or delete "
                                                          "another user "
                                                          "account.")
        return obj
