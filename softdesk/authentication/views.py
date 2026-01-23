from rest_framework.viewsets import ModelViewSet

from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(ModelViewSet):
    """ ViewSet for viewing and editing user """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
