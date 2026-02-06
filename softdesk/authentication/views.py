from django.contrib.auth import get_user_model
from django.views.defaults import permission_denied
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from .serializers import CustomUserSerializer

User = get_user_model()


@extend_schema_view(
    list=extend_schema(summary="Users list", tags=["Users"]),
    create=extend_schema(summary="Create a user", tags=["Users"]),
    retrieve=extend_schema(summary="Get user details", tags=["Users"]),
    update=extend_schema(summary="Update a user", tags=["Users"]),
    destroy=extend_schema(summary="Delete a user", tags=["Users"]),
)
class CustomUserViewSet(ModelViewSet):
    """ ViewSet for viewing and editing user """
    http_method_names = ['get', 'post', 'put', 'delete']
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
