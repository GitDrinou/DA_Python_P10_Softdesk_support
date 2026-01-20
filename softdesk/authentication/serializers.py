from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """ Serializer for our custom user model """
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'age',
            'can_be_contacted',
            'can_data_be_shared'
        ]
