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
        self.assertEqual(response_token.status_code, 401)

    def test_if_user_token_is_not_valid_raises_401_unauthorized(self) -> None:
        user = self.make_new_user().json()
        user_object: User | None = self.get_user_object(user['email'])
        other_user_object: User = self.make_user_object()
        user_token: str = token_email_generator.make_token(other_user_object)

        confirm_email_url = reverse('users:confirm_email', args=(
            self.encode_data(user_object.pk), user_token  # type: ignore
        ))

        expected_error_message: str = 'Your link to confirm your email address is invalid.'  # noqa: E501

        response: HttpResponse = self.client.get(
            confirm_email_url, follow=True
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn(expected_error_message, response.content.decode('utf-8'))

    def test_if_user_do_not_exists_raises_not_found(self) -> None:
        user = self.make_new_user().json()
        user_object: User | None = self.get_user_object(user['email'])
        user_token: str = token_email_generator.make_token(
            user_object  # type: ignore
        )
        confirm_email_url = reverse('users:confirm_email', args=(
            self.encode_data(uuid4()), user_token
        ))

        expected_error_message: str = 'User does not exist'

        response: HttpResponse = self.client.get(
            confirm_email_url, follow=True
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn(expected_error_message, response.content.decode('utf-8'))

    def test_if_new_user_try_to_get_your_data_without_access_token_returns_404(self) -> None:  # noqa: E501
        user = self.make_new_user().json()
        self.confirm_email(user['email'])

        response: HttpResponse = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_if_user_can_get_your_data_with_your_access_token(self) -> None:  # noqa: E501
        self.get_user_authenticated()

        response: HttpResponse = self.client.get(
            self.url, HTTP_AUTHORIZATION=self.auth_token
        )
        self.assertEqual(response.status_code, 200)

    def test_if_a_new_user_can_get_an_access_token(self) -> None:

        user = self.make_new_user().json()

        self.confirm_email(user['email'])

        response_token: HttpResponse = self.get_user_token(
            email=self.user_data['email'],
            password=self.user_data['password']
        )

        self.assertEqual(response_token.status_code, 200)

    def if_do_not_logged_user_try_to_update_your_data_returns_404(self) -> None:  # noqa: E501
        new_user_data: dict[str, str] = {
            'username': 'userNotLogged'
        }
        response: HttpResponse = self.client.put(
            self.url, data=new_user_data,
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 404)

    def test_if_logged_user_can_do_a_partial_update(self) -> None:
        self.get_user_authenticated()

        new_user_data: dict[str, str] = {
            'username': 'OtherUserName',
        }
        response: HttpResponse = self.client.patch(
            self.url, data=new_user_data, HTTP_AUTHORIZATION=self.auth_token,
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 200)

    def test_if_logged_user_can_do_a_full_update(self) -> None:
        self.get_user_authenticated()

        new_user_data: dict[str, str] = {
            'username': 'MyUserFTest',
            'email': 'userEmail123@email.com',
            'first_name': 'MyFirstName',
            'last_name': 'MyLastName',
            'password': '22@22#22',
        }
        response: HttpResponse = self.client.put(
            self.url, data=new_user_data, HTTP_AUTHORIZATION=self.auth_token,
            content_type=self.content_type
        )
        new_user_data.pop('password')
        response.json()

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), new_user_data)

    def test_if_do_not_logged_user_try_to_delete_returns_404(self) -> None:

        self.make_new_user()

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 404)

    def test_if_logged_user_can_delete_your_account(self) -> None:
        self.get_user_authenticated()

        response = self.client.delete(
            self.url,
            HTTP_AUTHORIZATION=self.auth_token
        )
        self.assertEqual(response.status_code, 204)
