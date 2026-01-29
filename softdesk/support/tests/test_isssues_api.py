from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from support.models import Project, Issue

User = get_user_model()


class IssueApiTests(APITestCase):
    def setUp(self):
        self.author = User.objects.create(
            username="author",
            password="pass123",
            first_name="author",
            last_name="soft",
            age=40)
        self.user1 = User.objects.create(
            username="user1",
            password="pass123",
            first_name="user1",
            last_name="Test",
            age=23
        )
        self.user2 = User.objects.create(
            username="user2",
            password="pass123",
            first_name="user2",
            last_name="Test",
            age=33
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='A test project',
            type='backend',
            author=self.author,
        )
        self.project.contributors.add(self.author, self.user1)
        self.issue = Issue.objects.create(
            author=self.author,
            name='Issue 1',
            description='New Description',
            priority='low',
            type='feature',
            status='todo',
            project=self.project,
        )

    def test_create_issue(self):
        self.client.force_authenticate(user=self.author)
        url = reverse('project-issue-list',
                      kwargs={'project_id': self.project.pk})
        payload = {
            'name': 'New Issue',
            'description': 'New Description',
            'priority': 'high',
            'type': 'feature',
            'status': 'todo',
            'project': self.project.pk,
            'comments': [],
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Issue.objects.count(), 2)

    def test_create_issue_by_user_not_author_or_contributor(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('project-issue-list',
                      kwargs={'project_id':  self.project.pk})
        payload = {
            'name': 'New Issue',
            'description': 'New Description',
            'priority': 'high',
            'type': 'feature',
            'status': 'todo',
            'project': self.project.pk,
            'comments': [],
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Issue.objects.count(), 1)

    def test_update_issue(self):
        self.client.force_authenticate(user=self.author)
        url = reverse('project-issue-detail',
                      kwargs={'project_id': self.project.pk,
                              'pk': self.issue.pk})
        payload = {
            'name': 'Issue 1 Updated',
            'description': 'New Description',
            'priority': 'low',
            'type': 'task',
            'status': 'todo',
            'project': self.project.pk,
            'author': self.author.pk,
            'comments': [],
        }
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Issue 1 Updated')

    def test_update_issue_patch(self):
        self.client.force_authenticate(user=self.author)
        url = reverse('project-issue-detail',
                      kwargs={'project_id': self.project.pk,
                              'pk': self.issue.pk})
        payload = {
            'priority': 'high',
        }
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['priority'], 'high')

    def test_delete_issue(self):
        self.client.force_authenticate(user=self.author)
        issue_detail_url = reverse(
            'project-issue-detail',
            kwargs={'project_id': self.project.pk, 'pk': self.issue.pk})
        response = self.client.delete(issue_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Issue.objects.filter(pk=self.issue.pk).exists())
