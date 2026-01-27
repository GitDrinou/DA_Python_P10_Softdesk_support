from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer

class IsAuthor(permissions.BasePermission):
    """Allows access only to authors"""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ProjectViewSet(ModelViewSet):
    """ ViewSet for viewing and editing project """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """ Return permissions based on action """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """ Create a new project with author as automatically a contributor"""
        project = serializer.save(author=self.request.user)
        project.contributors.add(self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


class ContributorViewSet(ModelViewSet):
    """ ViewSet for viewing and editing contributor """
    serializer_class = ContributorSerializer

    def get_queryset(self):
        """ Filter queryset by contributors """
        project_id = self.kwargs['project_id']
        return Contributor.objects.filter(project__id=project_id)
