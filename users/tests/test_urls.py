from django.test import TestCase
from django.urls import reverse


class UserUrlTestCase(TestCase):

    def test_user_url_is_correct(self) -> None:
        # The users views don`t allow the get method
        url: str = reverse('users:users')

        self.assertEqual(url, '/api/users/')
