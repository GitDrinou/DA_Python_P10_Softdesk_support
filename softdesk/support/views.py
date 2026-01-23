from rest_framework.viewsets import ModelViewSet

from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer


class ProjectViewSet(ModelViewSet):
    """ ViewSet for viewing and editing project """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

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
