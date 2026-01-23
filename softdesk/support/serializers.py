from django.contrib.auth import get_user_model
from rest_framework import serializers

from authentication.serializers import CustomUserSerializer
from .models import Project, Contributor

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    """ Serializer for project model """
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


class ContributorSerializer(serializers.ModelSerializer):
    """ Serializer for contributor model """
    class Meta:
        model = Contributor
        fields = '__all__'
