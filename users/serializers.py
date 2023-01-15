from collections import defaultdict
from typing import Dict, List

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from validators import EmailValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs) -> None:
        self._errors: Dict[str, List] = defaultdict(list)
        self._field: str

        return super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields: list[str] = [
            'username', 'first_name', 'last_name', 'email', 'password'
        ]
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    email = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True
    )

    def create(self, validated_data):

        validated_data['password'] = make_password(validated_data['password'])

        return super().create(validated_data)

    def update(self, instance, validated_data):

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name
        )
        instance.last_name = validated_data.get(
            'last_name', instance.last_name
        )

        password = validated_data.get("password", '')

        instance.password = make_password(password) if \
            password else instance.password

        instance.save()

        return instance

    def validate_username(self, value) -> str:
        self._field = 'username'
        if len(value) <= 2:
            self._errors[self._field].append(
                'Username must be at least 2 characters long'
            )
        if self._errors[self._field]:
            raise serializers.ValidationError(self._errors[self._field])

        return value

    def validate_email(self, value) -> str:
        self._field = 'email'
        if not EmailValidator(value).is_valid():
            self._errors[self._field].append(
                'Email must be a valid email address'
            )

        if self._errors[self._field]:
            raise serializers.ValidationError(self._errors[self._field])

        return value
