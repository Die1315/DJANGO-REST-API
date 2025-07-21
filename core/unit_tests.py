from datetime import date, timedelta

from django.test import TestCase

from core.models import Project
from core.serializers import ProjectSerializer


class TestProject(TestCase):
    def test_project_creation(self):
        project = Project.objects.create(name='Test Project', description='Test Description',
                                         start_date=date.today(), end_date=date.today() + timedelta(days=30))
        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(project.description, 'Test Description')
        self.assertEqual(project.start_date, date.today())
        self.assertEqual(project.end_date, date.today() + timedelta(days=30))

    def test_project_str(self):
        project = Project.objects.create(name='Test Project', description='Test Description',
                                         start_date=date.today(), end_date=date.today() + timedelta(days=30))
        self.assertEqual(str(project), 'Test Project')


class TestProjectSerializer(TestCase):
    def test_project_serializer(self):
        project = Project.objects.create(name='Test Project', description='Test Description',
                                         start_date=date.today(), end_date=date.today() + timedelta(days=30))
        serializer = ProjectSerializer(project)
        data = serializer.data
        self.assertEqual(data['name'], 'Test Project')
        self.assertEqual(data['description'], 'Test Description')
        self.assertEqual(data['start_date'], str(date.today()))
        self.assertEqual(data['end_date'], str(date.today() + timedelta(days=30)))
