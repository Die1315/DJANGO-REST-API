from django.test import TestCase

from users.models import Group


class TestGroup(TestCase):
    def test_group_creation(self):
        group = Group.objects.create(name='Test Group')
        self.assertEqual(group.name, 'Test Group')
