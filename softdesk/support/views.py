from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound, PermissionDenied
from django.db.models import Prefetch

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
        return Project.objects.filter(id=project_id,
                                      author=request.user).exists()

@extend_schema_view(
    list=extend_schema(summary="Projects list",tags=["Project"]),
    create=extend_schema(summary="Create a project", tags=["Project"]),
    retrieve=extend_schema(summary="Get project details", tags=["Project"]),
    update=extend_schema(summary="Update a project", tags=["Project"]),
    destroy=extend_schema(summary="Delete a project", tags=["Project"]),
)
class ProjectViewSet(ModelViewSet):
    """ ViewSet for viewing and editing project """
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Project.objects
            .filter(contributors=self.request.user)
            .select_related("author")
            .prefetch_related(Prefetch("contributors",
                                       queryset=User.objects.only("id")))
        )

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


@extend_schema_view(
    list=extend_schema(summary="Contributors list", tags=["Contributors"]),
    create=extend_schema(summary="Add a contributor to a project", tags=[
        "Contributors"]),
    retrieve=extend_schema(summary="Get contributor details",
                           tags=["Contributors"]),
    destroy=extend_schema(tags=["Contributors"]),
)
class ProjectContributorViewSet(ModelViewSet):
    """ ViewSet for viewing and editing project contributors """
    http_method_names = ['get', 'post', 'delete']
    serializer_class = CustomUserSerializer
    lookup_field = "pk"
    lookup_value_regex = r"\d+"

    def get_project(self):
        return get_object_or_404(
            Project.objects.filter(contributors=self.request.user),
            id=self.kwargs["project_id"]
        )

    def get_queryset(self):
        """ Restrict the queryset based on project contributors """
        project = self.get_project()
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

        if not project.contributors.filter(pk=user.pk).exists():
            project.contributors.add(user)

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['project_id'],
                                    author=request.user)
        user = get_object_or_404(User, id=kwargs['pk'])
        project.contributors.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=extend_schema(summary="Issues list", tags=["Issues"]),
    create=extend_schema(summary="Create an issue", tags=["Issues"]),
    retrieve=extend_schema(summary="Get issue details", tags=["Issues"]),
    update=extend_schema(summary="Update an issue", tags=["Issues"]),
    destroy=extend_schema(summary="Delete an issue", tags=["Issues"]),
)
class IssueViewSet(ModelViewSet):
    """ ViewSet for viewing and editing issue """
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Restrict the queryset based on action """
        project_id = self.kwargs.get('project_id')
        if not project_id:
            return Issue.objects.none()

        return (Issue.objects
                .filter(project__id=project_id,
                        project__contributors=self.request.user)
                .select_related('author', 'assigned_to', 'project')
                .prefetch_related('comments'))

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

        if not project.contributors.filter(pk=self.request.user.pk).exists():
            raise PermissionDenied(
                "You are not a contributor to this project."
            )
        serializer.save(author=self.request.user, project=project)


@extend_schema_view(
    list=extend_schema(summary="Comments list", tags=["Comments"]),
    create=extend_schema(summary="Create a comment", tags=["Comments"]),
    retrieve=extend_schema(summary="Get comment details", tags=["Comments"]),
    update=extend_schema(summary="Update a comment", tags=["Comments"]),
    destroy=extend_schema(summary="Delete a comment", tags=["Comments"]),
)
class CommentViewSet(ModelViewSet):
    """ ViewSet for viewing and editing comment """
    http_method_names = ['get', 'post', 'put', 'delete']
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
        return (Comment.objects
                .filter(
                    issue__id=issue_id,
                    issue__project__id=project_id,
                    issue__project__contributors=self.request.user)
                .select_related('author', 'issue', 'issue__project'))

    def perform_create(self, serializer):
        """ Create a new comment with author as automatically """
        issue_id = self.kwargs.get('issue_id')
        issue = get_object_or_404(Issue, id=issue_id)
        if not (issue.project.contributors
                .filter(pk=self.request.user.pk)
                .exists()):
            raise PermissionDenied(
                "You are not a contributor to this project."
            )
        serializer.save(author=self.request.user, issue=issue)
