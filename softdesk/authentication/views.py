from rest_framework import viewsets

from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing user """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

