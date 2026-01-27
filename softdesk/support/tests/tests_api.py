from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from authentication.models import CustomUser
from ..models import Project


class ProjectsApiTest(APITestCase):
    """ Tests for api action for project"""
    def setUp(self):
        self.list_url = reverse('project-list')
        self.user1 = CustomUser.objects.create_user(
            username="test-user",
            password="pass123",
            first_name="Test",
            last_name="User",
            age=25
        )
        self.user2 = CustomUser.objects.create_user(
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

    def test_create_project_with_authentification(self):
        self.client.force_authenticate(user=self.user1)
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
        self.assertIn("id", response.data)

        created_project = Project.objects.get(id=response.data["id"])
        self.assertEqual(created_project.name, "project3")
        self.assertEqual(created_project.type, "backend")
        self.assertEqual(created_project.author, self.user1)

        projects = Project.objects.all()
        self.assertEqual(len(projects), 3)

    def test_list_projects_with_authentification(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        projects = Project.objects.all()
        projects_names = {p.name for p in projects}
        self.assertSetEqual(projects_names, {"project1", "project2"})

    def test_retrieve_project_with_no_authentification(self):
        project1_detail_url = reverse(
            'project-detail',
            args=[self.project1.pk])
        response = self.client.get(project1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_project_with_authentification(self):
        self.client.force_authenticate(user=self.user1)
        project1_detail_url = reverse(
            'project-detail',
            args=[self.project1.pk])
        response = self.client.get(project1_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "project1")
        self.assertEqual(response.data["type"], "backend")

    def test_update_user_put(self):
        self.client.force_authenticate(user=self.user1)
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
        self.assertEqual(response.data["type"], "ios")

    def test_update_project_patch(self):
        self.client.force_authenticate(user=self.user1)
        project1_detail_url = reverse(
            'project-detail',
            args=[self.project1.pk])
        payload = {
            "type": "android",
        }
        response = self.client.patch(project1_detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["type"], "android")

    def test_delete_project_by_author(self):
        self.client.force_authenticate(user=self.user1)
        project2_detail_url = reverse(
            'project-detail',
            args=[self.project2.pk])
        response = self.client.delete(project2_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(pk=self.project2.pk).exists())

    def test_delete_project_not_by_author(self):
        self.client.force_authenticate(user=self.user2)
        project2_detail_url = reverse(
            'project-detail',
            args=[self.project2.pk])
        response = self.client.delete(project2_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Project.objects.filter(pk=self.project2.pk).exists())

    def test_unknown_project(self):
        self.client.force_authenticate(user=self.user1)
        project_detail_url = reverse('project-detail', args=[00])
        response = self.client.get(project_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
