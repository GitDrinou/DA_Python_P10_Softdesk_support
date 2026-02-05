from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from .serializers import CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(ModelViewSet):
    """ ViewSet for viewing and editing user """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        """ Return permissions based on action """
        if self.action in ['create']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return User.objects.filter(is_staff=False)

    def get_object(self):
        obj = super().get_object()
        if obj != self.request.user:
            raise PermissionDenied("You are not authorized to update or "
                                   "delete another user account.")
        return obj
