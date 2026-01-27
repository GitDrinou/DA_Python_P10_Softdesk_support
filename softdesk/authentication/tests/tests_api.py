from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from ..models import CustomUser


class CustomUserApiTest(APITestCase):
    """ Tests for api action for user"""
    def setUp(self):
        self.list_url = reverse('user-list')
        self.user1 = CustomUser.objects.create_user(
            username="user1",
            password="pass123",
            first_name="John",
            last_name="Doe",
            age=21,
            can_be_contacted=True,
            can_data_be_shared=False,
        )
        self.user2 = CustomUser.objects.create_user(
            username="user2",
            password="pass123",
            first_name="Jane",
            last_name="Doe",
            age=19,
            can_be_contacted=False,
            can_data_be_shared=False,
        )

    def test_create_user(self):
        payload = {
            "username": "user-test-create",
            "first_name": "Bob",
            "last_name": "Doe",
            "age": 15,
            "can_be_contacted": True,
            "can_data_be_shared": False,
        }

        response = self.client.post(
            self.list_url,
            data=payload,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

        created_user = CustomUser.objects.get(id=response.data["id"])
        self.assertEqual(created_user.username, "user-test-create")
        self.assertEqual(created_user.age, 15)
        self.assertTrue(created_user.can_be_contacted)
        self.assertFalse(created_user.can_data_be_shared)

        users = CustomUser.objects.all()
        self.assertEqual(len(users), 3)

    def test_list_user_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        users = CustomUser.objects.all()
        usernames = {u.username for u in users}
        self.assertSetEqual(usernames, {"user1", "user2"})

    def test_retrieve_user_unauthenticated(self):
        user1_detail_url = reverse('user-detail', args=[self.user1.pk])
        response = self.client.get(user1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        user1_detail_url = reverse('user-detail', args=[self.user1.pk])
        response = self.client.get(user1_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "user1")
        self.assertEqual(response.data["age"], 21)
        self.assertTrue(response.data["can_be_contacted"])

    def test_update_user_put(self):
        self.client.force_authenticate(user=self.user1)
        user1_detail_url = reverse('user-detail', args=[self.user1.pk])
        payload = {
            "username": "user1-new",
            "first_name": "Justin",
            "last_name": "Blue",
            "age": 30,
            "can_be_contacted": False,
            "can_data_be_shared": False,
        }

        response = self.client.put(user1_detail_url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "user1-new")
        self.assertEqual(response.data["first_name"], "Justin")
        self.assertEqual(response.data["age"], 30)
        self.assertFalse(response.data["can_be_contacted"])
        self.assertFalse(response.data["can_data_be_shared"])

    def test_update_user_patch(self):
        self.client.force_authenticate(user=self.user1)
        user1_detail_url = reverse('user-detail', args=[self.user1.pk])
        payload = {
            "age": 40,
            "can_be_contacted": False,
        }
        response = self.client.patch(user1_detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["age"], 40)
        self.assertFalse(response.data["can_be_contacted"])

    def test_delete_user(self):
        self.client.force_authenticate(user=self.user2)
        user2_detail_url = reverse('user-detail', args=[self.user2.pk])
        response = self.client.delete(user2_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(pk=self.user2.pk).exists())

    def test_unknown_user(self):
        self.client.force_authenticate(user=self.user1)
        user_detail_url = reverse('user-detail', args=[000000])
        response = self.client.get(user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
