from rest_framework import serializers

from .models import Team, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 'password', 'teams'
        ]


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(
        many=True,
        queryset=User.objects.all(),
        slug_field='email',
        required=False,
        allow_empty=True
    )

    class Meta:
        model = Team
        fields = ['id', 'name', 'members']
