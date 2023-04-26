from typing import Union

from django.http import HttpResponse
from django.urls import reverse

from users.models import User
from utils.tokens import token_email_generator

from .test_base import IntegrationBaseTestCase


class UserTokenIntegrationTestCase(IntegrationBaseTestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        return super().__init__(methodName)

    def test_if_user_can_get_a_pair_token(self) -> None:
        user: User = User.objects.create(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email="johndoe@example.com",
        )
        user.set_password('2288773@@1')
        user.is_active = True
        user.save()

        response = self.client.post(self.token_pair_url, data={
            "email": user.email,
            "password": '2288773@@1'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_if_new_user_try_to_get_your_data_without_access_token_returns_404(self) -> None:  # noqa: E501
        user = self.make_new_user().json()
        self.confirm_email(user['email'])

        response: HttpResponse = self.client.get(self.user_url)

        self.assertEqual(response.status_code, 401)

    def test_if_user_token_is_not_valid_raises_401_unauthorized(self) -> None:
        user = self.make_new_user().json()
        user_object: Union[User, None] = self.get_user_object(user['email'])
        other_user_object: User = self.make_user_object()
        user_token: str = token_email_generator.make_token(other_user_object)

        confirm_email_url = reverse('users:confirm_email', args=(
            self.encode_data(user_object.pk), user_token  # type: ignore
        ))

        expected_error_message: str = 'Your link to confirm your email address is invalid.'  # noqa: E501

        response: HttpResponse = self.client.get(
            confirm_email_url, follow=True
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(expected_error_message, response.content.decode('utf-8'))

    def test_if_user_can_get_your_data_with_your_access_token(self) -> None:  # noqa: E501
        self.get_user_authenticated()

        response: HttpResponse = self.client.get(
            self.user_url, HTTP_AUTHORIZATION=self.auth_token
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

    def test_if_logged_user_can_do_a_partial_update(self) -> None:
        self.get_user_authenticated()

        new_user_data: dict[str, str] = {
            'username': 'OtherUserName',
        }
        response: HttpResponse = self.client.patch(
            self.user_url, data=new_user_data,
            HTTP_AUTHORIZATION=self.auth_token,
            content_type="application/json"
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
            self.user_url, data=new_user_data,
            HTTP_AUTHORIZATION=self.auth_token,
            content_type=self.content_type
        )

        new_user_data.pop('password')

        response_data = response.json()
        response_data.pop('email_verified')

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response_data, new_user_data)

    def test_if_logged_user_can_delete_your_account(self) -> None:
        self.get_user_authenticated()

        response: HttpResponse = self.client.delete(
            self.user_url,
            HTTP_AUTHORIZATION=self.auth_token
        )
        self.assertEqual(response.status_code, 204)

    def test_if_user_can_get_a_new_access_token_with_your_refresh_token(self) -> None:  # noqa: E501
        user: HttpResponse = self.make_new_user(
            email="emailtojohn@gmail.com",
            username="John",
            password="jonh23422"
        ).json()

        self.confirm_email(user['email'])

        token_response: HttpResponse = self.get_user_token(
            email=user['email'],
            password="jonh23422"
        ).json()

        response: HttpResponse = self.client.post(
            self.refresh_token_url, data={
                'refresh': token_response['refresh']
            })

        self.assertEqual(response.status_code, 200)

    def test_if_user_try_get_a_new_access_token_without_send_refresh_token_return_400(self) -> None:  # noqa: E501
        user: HttpResponse = self.make_new_user(
            email="emailtojohn@gmail.com",
            username="John",
            password="jonh23422"
        ).json()

        self.confirm_email(user['email'])

        response: HttpResponse = self.client.post(
            self.refresh_token_url, data={
            })

        self.assertEqual(response.status_code, 400)
