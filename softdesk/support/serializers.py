from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Project, Issue, Comment

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


class IssueSerializer(serializers.ModelSerializer):
    """ Serializer for issue model """
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id',
            'author',
            'project',
            'assigned_to',
            'name',
            'description',
            'priority',
            'type',
            'status',
            'created_time',
            'comments'
        ]


class CommentSerializer(serializers.ModelSerializer):
    """ Serializer for issue model """
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    issue = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'issue',
            'author',
            'description',
            'created_time',
        ]
