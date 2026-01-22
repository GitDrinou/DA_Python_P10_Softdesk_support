from django.contrib.auth import get_user_model
from django.db import models

from softdesk.softdesk import settings

User = get_user_model()


class Project(models.Model):
    """ Project model """
    TYPE_CHOICES = (
        ('backend', 'back-end'),
        ('frontend', 'front-end'),
        ('ios', 'IOS'),
        ('android', 'Android'),
    )
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2048)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)
    contributors = models.ManyToManyField(User,
                                          related_name='contributors')

    def __str__(self):
        return f'{self.name} ({self.type}) du {self.created_time}'


class Contributor(models.Model):
    """ Contributor model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f'Contributeur: {self.user.username} du {self.project.name}'
