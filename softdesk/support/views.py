from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound

from authentication.serializers import CustomUserSerializer
from .models import Project, Issue, Comment
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer

User = get_user_model()


class IsAuthorOrContributor(permissions.BasePermission):
    """Allows access only to authors"""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsProjectAuthor(permissions.BasePermission):
    """Allows access only to project authors"""
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id')
        if not project_id:
            return False

        try:
            project = Project.objects.get(id=project_id)
            return project.author == request.user
        except Project.DoesNotExist:
            return False


class ProjectViewSet(ModelViewSet):
    """ ViewSet for viewing and editing project """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """ Return permissions based on action """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthorOrContributor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """ Create a new project with author as automatically a contributor"""
        project = serializer.save(author=self.request.user)
        project.contributors.add(self.request.user)


class ProjectContributorViewSet(ModelViewSet):
    """ ViewSet for viewing and editing project contributors """
    serializer_class = CustomUserSerializer
    lookup_field = "pk"
    lookup_value_regex = r"\d+"

    def get_queryset(self):
        """ Restrict the queryset based on project contributors """
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        return project.contributors.all()

    def get_permissions(self):
        """ Return permissions based on action """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsProjectAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['project_id'])
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)
        project.contributors.add(user)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['project_id'])
        user = get_object_or_404(User, id=kwargs['pk'])
        project.contributors.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewSet(ModelViewSet):
    """ ViewSet for viewing and editing issue """
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Restrict the queryset based on action """
        project_id = self.kwargs.get('project_id')
        if not project_id:
            return Issue.objects.none()

        return Issue.objects.filter(project__id=project_id)

    def get_permissions(self):
        """ Return permissions based on action """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthorOrContributor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        """ Project injection to serializer for validation (create) """
        context = super().get_serializer_context()
        project_id = self.kwargs.get('project_id')
        if project_id:
            try:
                context['project'] = get_object_or_404(Project, id=project_id)
            except Project.DoesNotExist:
                context['project'] = None
        return context

    def perform_create(self, serializer):
        """ Create a new issue with an author automatically"""
        project = self.get_serializer_context().get("project")
        if project is None:
            raise NotFound("Project does not exist")

        if self.request.user not in project.contributors.all():
            raise permissions.exceptions.PermissionDenied("You are not a "
                                                          "contributor to "
                                                          "this project.")
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(ModelViewSet):
    """ ViewSet for viewing and editing comment """
    serializer_class = CommentSerializer
    lookup_field = "pk"

    def get_permissions(self):
        """ Return permissions based on action """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthorOrContributor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """ Restrict the queryset based on action """
        project_id = self.kwargs.get('project_id')
        issue_id = self.kwargs.get('issue_id')
        return Comment.objects.filter(
            issue__id=issue_id,
            issue__project__id=project_id,
            issue__project__contributors=self.request.user
        )

    def perform_create(self, serializer):
        """ Create a new comment with author as automatically """
        issue_id = self.kwargs.get('issue_id')
        issue = get_object_or_404(Issue, id=issue_id)
        if self.request.user not in issue.project.contributors.all():
            raise permissions.exceptions.PermissionDenied("You are not a "
                                                          "contributor to "
                                                          "this project.")
        serializer.save(author=self.request.user, issue=issue)
