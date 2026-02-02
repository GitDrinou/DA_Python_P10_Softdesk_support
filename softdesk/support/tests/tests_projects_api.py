from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from ..models import Project

User = get_user_model()


class ProjectsApiTest(APITestCase):
    """ Tests for api action for project"""
    def setUp(self):
        self.list_url = reverse('project-list')
        self.user1 = User.objects.create_user(
            username="test-user",
            password="pass123",
            first_name="Test",
            last_name="User",
            age=25
        )
        self.user2 = User.objects.create_user(
            username="test-user2",
            password="pass123",
            first_name="Test",
            last_name="User2",
            age=35
        )
        self.project1 = Project.objects.create(
            author=self.user1,
            name="project1",
            description="description1",
            type="backend")
        self.project2 = Project.objects.create(
            author=self.user1,
            name="project2",
            description="description2",
            type="frontend")
        self.project1.contributors.add(self.user1)
        self.project2.contributors.add(self.user1)

    def auth(self, user):
        self.client.force_authenticate(user=user)

    def test_create_project_with_authentification(self):
        self.auth(self.user1)
        payload = {
            "name": "project3",
            "description": "description3",
            "type": "backend",
        }
        response = self.client.post(
            self.list_url,
            data=payload,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_project = Project.objects.get(id=response.data["id"])
        self.assertEqual(created_project.author, self.user1)
        self.assertEqual(created_project.name, "project3")
        self.assertTrue(created_project.contributors.filter(
            pk=self.user1.pk).exists())

    def test_list_projects_with_authentification(self):
        self.auth(self.user1)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get("results", response.data)
        name = {p["name"] for p in data}
        self.assertSetEqual(name, {"project1", "project2"})

    def test_retrieve_project_unauthenticated(self):
        project1_detail_url = reverse(
            'project-detail',
            args=[self.project1.pk])

        response = self.client.get(project1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_project_authenticated_contributor(self):
        self.auth(self.user1)
        project1_detail_url = reverse(
            'project-detail',
            args=[self.project1.pk])

        response = self.client.get(project1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "project1")

    def test_retrieve_project_authenticated_not_contributor_returns_404(self):
        self.auth(self.user2)
        url = reverse("project-detail", args=[self.project2.pk])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_put_by_author(self):
        self.auth(self.user1)
        project1_detail_url = reverse(
            'project-detail',
            args=[self.project1.pk])

        payload = {
            "name": "project1-new",
            "description": "new description here",
            "type": "ios",
        }
        response = self.client.put(project1_detail_url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "project1-new")

    def test_delete_project_by_author(self):
        self.auth(self.user1)
        project2_detail_url = reverse(
            'project-detail',
            args=[self.project2.pk])
        response = self.client.delete(project2_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(pk=self.project2.pk).exists())

    def test_delete_project_not_contributor_or_return_404(self):
        self.auth(self.user2)
        project2_detail_url = reverse(
            'project-detail',
            args=[self.project2.pk])
        response = self.client.delete(project2_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Project.objects.filter(pk=self.project2.pk).exists())

    def test_unknown_project_returns_404(self):
        self.auth(self.user1)
        url = reverse("project-detail", args=[999999])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
