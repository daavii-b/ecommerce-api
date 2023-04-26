import os
from typing import Dict, Tuple, Union

from django.conf import settings
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from utils.coders import Coders
from utils.tokens import token_email_generator

from ..models import User


class UserBaseTestCase(TestCase):
    def __init__(self, *args, **kwargs) -> None:
        self.auth_token = 'Bearer '
        self.url: str = reverse('users:users')
        self.token_url: str = reverse('tokens:pair-tokens')
        self.content_type = 'application/json'
        self.email_dir = os.path.join(
            settings.BASE_DIR, settings.MEDIA_ROOT, 'emails'
        )
        self._coder = Coders()

        super().__init__(*args, **kwargs)

    def setUp(self) -> None:
        self.user_data: dict = self.get_user_data()
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def confirm_email(self, email: str) -> HttpResponse:
        return self.client.get(
            self.get_confirm_email_url(
                self.get_user_object(email)
            ),
            follow=True
        )

    def get_confirm_email_url(self, user: Union[User, None]) -> str:
        return reverse(
            'users:confirm_email',
            args=self.get_encoded_data(user)
        ) if user else ''

    def get_encoded_data(self, user) -> Tuple[str, str]:
        return (
            self._coder.encode(user.pk), token_email_generator.make_token(user)
        )

    def make_new_user(
        self,
        username: str = '',
        email: str = '',
        password: str = '',
    ) -> HttpResponse:
        return self.client.post(self.url, data={
            'email': email or self.user_data['email'],
            'password': password or self.user_data['password'],
            'username': username or self.user_data['username'],
        })

    def get_user_token(
        self,
        email: str,
        password: str,
    ) -> HttpResponse:
        return self.client.post(self.token_url, data={
            'email': email,
            'password': password,
        })

    def encode_data(self, data) -> str:
        return self._coder.encode(data)

    @staticmethod
    def make_user_object(
        first_name: str = 'FirstNameTest',
        last_name: str = 'LastNameTest',
        username: str = 'UserTester',
        email: str = 'emailtotest@gmail.com',
        password: str = 'passTotester12'
    ) -> User:
        return User.objects.create_user(  # type: ignore
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )

    @staticmethod
    def get_user_object(email: str) -> Union[User, None]:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user_data() -> Dict[str, str]:
        return {
            'email': 'defaultEmail@example.com',
            'username': 'defaultUsername',
            'password': '23444',
        }

    def get_user_authenticated(
            self) -> Dict[str, Dict[str, str]]:
        user_data: Dict[str, str] = self.get_user_data()

        user = self.make_new_user(**user_data).json()

        self.confirm_email(user['email'])

        user_token: HttpResponse = self.get_user_token(
            user_data['email'], user_data['password']
        )

        self.auth_token += user_token.json().get('access', '')

        return {
            **user,
        }
