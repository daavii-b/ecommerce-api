from typing import Dict

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class UserBaseTestCase(TestCase):
    def __init__(self, *args, **kwargs) -> None:
        self.auth_token = 'Bearer '
        self.url: str = reverse('users:users')
        self.token_url: str = reverse('token_obtain_pair')
        super().__init__(*args, **kwargs)

    def make_new_user(
        self,
        username: str,
        email: str,
        password: str,
    ) -> HttpResponse:
        return self.client.post(self.url, data={
            'email': email,
            'password': password,
            'username': username,
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

    @ staticmethod
    def get_user_data() -> Dict[str, str]:
        return {
            'email': 'britodavi122@gmail.com',
            'username': 'myusername',
            'password': '23444',
        }

    def get_user_authenticated(
            self) -> Dict[str, Dict[str, str]]:
        user_data: Dict[str, str] = self.get_user_data()

        user = self.make_new_user(**user_data)

        user_token: HttpResponse = self.get_user_token(
            user_data['email'], user_data['password']
        )

        self.auth_token += user_token.json().get('access', '')
        return {
            **user.json(),
        }
