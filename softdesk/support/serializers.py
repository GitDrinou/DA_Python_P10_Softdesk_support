from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Project

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    """ Serializer for project model """
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'author',
            'name',
            'description',
            'type',
            'created_time',
            'contributors'
        ]
