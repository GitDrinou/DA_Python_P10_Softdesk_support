import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Project(models.Model):
    """ Project model """
    TYPE_CHOICES = (
        ('backend', 'back-end'),
        ('frontend', 'front-end'),
        ('ios', 'IOS'),
        ('android', 'Android'),
    )
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2048)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)
    contributors = models.ManyToManyField(User,
                                          related_name='projects', blank=True)

    def __str__(self):
        return f'{self.name} ({self.type}) du {self.created_time}'


class Issue(models.Model):
    """ Issue model """
    PRIORITY_CHOICES = (
        ('low', 'low'),
        ('medium', 'medium'),
        ('high', 'high'),
    )
    TYPE_CHOICES = (
        ('bug', 'bug'),
        ('feature', 'feature'),
        ('task', 'task'),
    )
    STATUS_CHOICES = (
        ('todo', 'to do'),
        ('progress', 'in progress'),
        ('finished', 'finished'),
    )
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True,
                               related_name='authored_issues')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE,
                                related_name='issues')
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2048)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='todo')
    assigned_to = models.ForeignKey(to=User, on_delete=models.SET_NULL,
                                    related_name='assigned_issues',
                                    null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.type}) du {self.created_time}'


class Comment(models.Model):
    """ Comment model """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    issue = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        related_name='comments')
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL,
                               null=True, related_name='comments')
    description = models.TextField(max_length=2048)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.issue} by ({self.author}) on {self.created_time}'
