from collections import defaultdict
from typing import Dict, List

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User
from .validators import EmailValidator


class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs) -> None:
        self._errors: Dict[str, List] = defaultdict(list)
        self._field: str
        return super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

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

        password = validated_data.get("password", '')

        instance.password = make_password(password) if \
            password else instance.password

        instance.save()

        return instance

    def validate_username(self, value):
        self._field = 'username'
        if len(value) <= 2:
            self._errors[self._field].append(
                'Username must be at least 2 characters long'
            )
        if self._errors[self._field]:
            raise serializers.ValidationError(self._errors[self._field])

        return value

    def validate_email(self, value):
        self._field = 'email'
        if not EmailValidator(value).is_valid():
            self._errors[self._field].append(
                'Email must be a valid email address'
            )

        if self._errors[self._field]:
            raise serializers.ValidationError(self._errors[self._field])

        return value
