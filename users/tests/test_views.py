from uuid import uuid4

from django.http import HttpResponse
from django.test import override_settings
from django.urls import reverse

from utils.tokens import token_email_generator

from ..models import User
from .test_base import UserBaseTestCase


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_STORE_EAGER_RESULT=True,
)
class UserViewTestCase(UserBaseTestCase):

    def test_if_new_user_can_create_an_account(self) -> None:
        response: HttpResponse = self.make_new_user()

        self.assertEqual(response.status_code, 201)

    def test_if_user_cannot_make_login_without_confirm_your_email(self) -> None:  # noqa: E501

        self.make_new_user(**self.user_data)

        response_token = self.get_user_token(
            self.user_data['email'], self.user_data['password']
        )
        self.assertEqual(response_token.status_code, 400)

    def test_if_user_can_resend_the_email_to_confirmation(self) -> None:
        user: User = self.make_user_object(email='test@example.com')

        url: str = reverse('users:resend_confirmation_email', kwargs={
            'username': user.username,
        })

        response: HttpResponse = self.client.get(url)

        self.confirm_email(user.email)

        self.assertEqual(response.status_code, 200)

    def test_if_user_that_not_exists_resend_the_email_to_confirmation_returns_404(self) -> None:  # noqa: E501

        url: str = reverse('users:resend_confirmation_email', kwargs={
            'username': 'UserDoNotExist',
        })

        response: HttpResponse = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_if_user_do_not_exists_raises_not_found(self) -> None:
        user: dict = self.make_new_user().json()
        user_object: User | None = self.get_user_object(user['email'])
        user_token: str = token_email_generator.make_token(
            user_object  # type: ignore
        )
        confirm_email_url: str = reverse('users:confirm_email', args=(
            self.encode_data(uuid4()), user_token
        ))

        expected_error_message: str = 'User does not exist'

        response: HttpResponse = self.client.get(
            confirm_email_url, follow=True
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn(expected_error_message, response.content.decode('utf-8'))

    def if_do_not_logged_user_try_to_update_your_data_returns_404(self) -> None:  # noqa: E501
        new_user_data: dict[str, str] = {
            'username': 'userNotLogged'
        }
        response: HttpResponse = self.client.put(
            self.url, data=new_user_data,
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 401)

    def test_if_do_not_logged_user_try_to_delete_returns_404(self) -> None:

        self.make_new_user()

        response: HttpResponse = self.client.delete(self.url)

        self.assertEqual(response.status_code, 401)
