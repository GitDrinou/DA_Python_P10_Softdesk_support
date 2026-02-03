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
        read_only_fields = ['author', 'created_time', 'project']

    def validate(self, attrs):
        """ Validate the assignee to be contributors to the project
            Args:
                attrs (dict): attributes of the issue model
        """
        if "assigned_to" not in attrs:
            return attrs

        assigned_to = attrs.get("assigned_to")
        if assigned_to is None:
            return attrs

        if self.instance is not None:
            project = self.instance.project
        else:
            project = self.context.get("project")

        if project is None:
            raise serializers.ValidationError(
                "Project not found to validate the assignment"
            )

        if assigned_to and not project.contributors.filter(
                pk=assigned_to).exists():
            raise serializers.ValidationError(
                {"assigned_to": "The assignee user must be a project "
                                "contributor"}
            )

        return attrs


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
