from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from support.models import Project, Issue, Comment

User = get_user_model()


class CommentApiTests(APITestCase):
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
            age=23)
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
        self.comment = Comment.objects.create(
            author=self.author,
            issue=self.issue,
            description='New Issue Comment Description',
        )

    def test_create_issue_comment(self):
        self.client.force_authenticate(user=self.author)
        url = reverse('project-issue-comment-list',
                      kwargs={'project_id': self.project.pk,
                              'issue_id': self.issue.pk})
        payload = {
            'description': 'New issue comment Description',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_create_issue_comment_by_user_not_author_or_contributor(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('project-issue-comment-list',
                      kwargs={'project_id': self.project.pk,
                              'issue_id': self.issue.pk})
        payload = {
            'description': 'New Issue Comment Description',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Issue.objects.count(), 1)

    def test_update_issue_comment(self):
        self.client.force_authenticate(user=self.author)
        url = reverse('project-issue-comment-detail',
                      kwargs={'project_id': self.project.pk,
                              'issue_id': self.issue.pk,
                              'pk': self.comment.pk})
        payload = {
            'description': 'New Description updated',
        }
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'New Description '
                                                       'updated')

    def test_delete_issue_comment(self):
        self.client.force_authenticate(user=self.author)
        url = reverse('project-issue-comment-detail',
                      kwargs={'project_id': self.project.pk,
                              'issue_id': self.issue.pk,
                              'pk': self.comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Issue.objects.filter(pk=self.comment.pk).exists())
