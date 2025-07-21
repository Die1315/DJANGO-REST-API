from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate_password(self, value) -> str:
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long")
        return value

    def validate_password_confirmation(self, value) -> str:
        if value != self.initial_data.get('password'):
            raise serializers.ValidationError(
                "Password confirmation does not match")
        return value

    def validate(self, data) -> dict:
        self.validate_password_confirmation(data['password_confirmation'])
        self.validate_password(data['password'])
        data.pop('password_confirmation')
        return data

    def create(self, validated_data) -> User:
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError(
                "User with this email already exists."
            )

        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data['password'],
            username=validated_data['email'],
        )

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data) -> dict:
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data
