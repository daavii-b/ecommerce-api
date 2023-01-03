from django.test import TestCase

from ..models import User


class ModelTesCase(TestCase):

    def test_if_str_method_return_the_username(self):
        username = 'username-test'

        user = User.objects.create(
            email='test@example.com', username=username, password='test123456'
        )

        self.assertEqual(str(user), username)
