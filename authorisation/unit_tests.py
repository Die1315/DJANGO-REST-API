from django.test import TestCase

from authorisation.serializers import RegisterSerializer


class TestSerializers(TestCase):
    def setUp(self):
        self.serializer = RegisterSerializer(data={
            'email': 'test@test.com',
            'password': 'testpassword',
            'password_confirmation': 'testpassword',
            'first_name': 'Test',
            'last_name': 'Test'
        })

    def test_register_serializer_valid(self):
        self.assertTrue(self.serializer.is_valid())
        self.assertEqual(self.serializer.validated_data['email'], 'test@test.com')
        self.assertEqual(self.serializer.validated_data['first_name'], 'Test')
        self.assertEqual(self.serializer.validated_data['last_name'], 'Test')

    def test_register_serializer_invalid(self):
        self.serializer = RegisterSerializer(data={})
        self.assertFalse(self.serializer.is_valid())
        self.assertEqual(self.serializer.errors['email'], ['This field is required.'])
        self.assertEqual(self.serializer.errors['password'], ['This field is required.'])
        self.assertEqual(self.serializer.errors['password_confirmation'], ['This field is required.'])
        self.assertEqual(self.serializer.errors['first_name'], ['This field is required.'])
        self.assertEqual(self.serializer.errors['last_name'], ['This field is required.'])
