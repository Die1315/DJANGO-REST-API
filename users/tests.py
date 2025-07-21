from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import Team, User


class TestGroup(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            username='test@example.com'
        )

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

    def test_group_creation(self):
        request = self.client.post(
            '/api/team/',
            {
                'name': 'Test Group'
            }
        )
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.data['name'], 'Test Group')

    def test_group_list(self):
        request = self.client.get('/api/team/')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data), 1)
        self.assertEqual(request.data[0]['name'], 'Test Team')

    def test_group_detail(self):
        request = self.client.get(f'/api/team/{self.team.id}/')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['name'], 'Test Team')

    def test_group_update(self):
        request = self.client.put(f'/api/team/{self.team.id}/', {
            'name': 'Updated Test Group'
        })

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['name'], 'Updated Test Group')

        team = Team.objects.get(id=self.team.id)
        self.assertEqual(team.name, 'Updated Test Group')

    def test_add_user_to_group(self):
        request = self.client.patch(f'/api/team/{self.team.id}/', {
            'members': [self.user.email]
        }, format='json')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['members'], [self.user.email])

    def test_remove_user_from_group(self):
        self.team.members.add(self.user)

        request = self.client.patch(f'/api/team/{self.team.id}/', data={
            'members': []
        }, format='json')

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['members'], [])
        self.assertEqual(Team.objects.get(id=self.team.id).members.count(), 0)
        self.assertEqual(Team.objects.get(id=self.team.id).members.first(), None)

    def test_group_delete(self):
        request = self.client.delete(f'/api/team/{self.team.id}/')
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.count(), 0)

    def test_unauthenticated_user(self):
        self.client.force_authenticate(user=None)
        request = self.client.get('/api/team/')
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)
