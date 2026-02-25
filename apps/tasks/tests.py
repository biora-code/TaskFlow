from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task


class TestTaskSecurity(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

        Task.objects.create(user=self.user1, title="User1 Task")

    def test_unauthorized_access(self):
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_data_isolation(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/tasks/')
        self.assertEqual(len(response.data['results']), 0)

    def test_generate_subtasks_requires_auth(self):
        task = Task.objects.create(
        title="Test",
        user=self.user1)
        response = self.client.post(
        f"/api/tasks/{task.id}/generate-subtasks/")
        self.assertEqual(response.status_code, 401)