from django.test import TestCase
from rest_framework import status

from users.models import User


class TestAuthorisation(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testdev@test.com',
            password='testpassword',
            first_name='Test',
            last_name='Test',
            username='testdev@test.com'
        )

    def test_register(self):
        response = self.client.post(
            '/api/register/',
            {
                'email': 'test@test.com',
                'password': 'testpassword',
                'password_confirmation': 'testpassword',
                'first_name': 'Test',
                'last_name': 'Test'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'test@test.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'Test')

    def test_register_with_existing_email(self):
        response = self.client.post(
            '/api/register/',
            {
                'email': 'testdev@test.com',
                'password': 'testpassword',
                'password_confirmation': 'testpassword',
                'first_name': 'Test',
                'last_name': 'Test'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0],
                         'User with this email already exists.')

    def test_login(self):
        response = self.client.post(
            '/api/login/',
            {
                'email': 'testdev@test.com',
                'password': 'testpassword'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['email'], 'testdev@test.com')
        token = response.data['token']
        self.assertIsNotNone(token)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(
            '/api/login/',
            {
                'email': 'test@test.com',
                'password': 'wrongpassword'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'Invalid credentials')
