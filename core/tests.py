from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Project
from users.models import User

# Create your tests here.


class TestProject(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            username='test@example.com'
        )

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Create a test project
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30)
        )

    def test_project_list(self):
        response = self.client.get(reverse('project-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Project')
        self.assertEqual(response.data[0]['description'], 'Test Description')
        self.assertEqual(response.data[0]['start_date'], str(date.today()))
        self.assertEqual(response.data[0]['end_date'], str(date.today() + timedelta(days=30)))

    def test_user_authentication(self):
        """Test that the user is properly authenticated"""
        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test without authentication
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('project-list'))
        # This might return 401 or 403 depending on your view permissions
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_project_endpoint_with_authorization(self):
        """Test the project endpoint with proper authorization"""
        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test GET request to specific project
        project_detail_url = reverse('project-detail', kwargs={'pk': self.project.pk})
        response = self.client.get(project_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test POST request to create new project
        new_project_data = {
            'name': 'New Test Project',
            'description': 'New Test Description',
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=60)
        }
        response = self.client.post(reverse('project-list'), new_project_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify the new project was created
        response = self.client.get(reverse('project-list'))
        self.assertEqual(len(response.data), 2)  # Original + new project
