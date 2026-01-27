from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from ..models import Project

User = get_user_model()


class ProjectContributorsApiTest(APITestCase):
    """ Tests for api action for project contributors"""
    def setUp(self):
        self.author = User.objects.create(
            username="test-user",
            password="pass123",
            first_name="Test",
            last_name="User",
            age=25
        )
        self.contributor1 = User.objects.create(
            username="contributor1",
            password="pass123",
            first_name="contributor1",
            last_name="Test",
            age=35
        )
        self.contributor2 = User.objects.create(
            username="contributor2",
            password="pass123",
            first_name="contributor2",
            last_name="Test",
            age=20
        )
        self.user1 = User.objects.create(
            username="user1",
            password="pass123",
            first_name="user1",
            last_name="Test",
            age=40
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='A test project',
            type='backend',
            author=self.author
        )
        self.project.contributors.add(self.author, self.contributor1)

    def list_contributors(self):
        url = reverse(
            'project-contributor-list',
            kwargs={'project_id': self.project.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_add_contributor(self):
        url = reverse(
            'project-contributor-list',
            kwargs={'project_id': self.project.pk})
        self.client.force_authenticate(user=self.author)
        payload = {
            "user_id": self.contributor2.pk,
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.contributor2, self.project.contributors.all())

    def test_remove_contributor(self):
        self.project.contributors.add(self.contributor2)
        url = reverse('project-contributor-detail',
                      kwargs={'project_id': self.project.pk,
                              'pk': self.contributor2.pk})
        self.client.force_authenticate(user=self.author)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(self.contributor2, self.project.contributors.all())
