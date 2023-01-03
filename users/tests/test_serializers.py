from typing import Dict

from rest_framework import serializers

from ..serializers import UserSerializer
from .test_user_base import UserBaseTestCase


class UserSerializerTestCase(UserBaseTestCase):

    def test_if_username_less_than_three_chars_raises_validation_error(self) -> None:  # noqa: E501

        with self.assertRaises(serializers.ValidationError):

            user_data: Dict[str, str] = self.get_user_data()
            user_data.update({'username': 'us'})
            serializer: UserSerializer = UserSerializer(data=user_data)
            serializer.is_valid(raise_exception=True)

    def test_if_invalid_email_raises_validation_error(self) -> None:

        with self.assertRaises(serializers.ValidationError):

            user_data: Dict[str, str] = self.get_user_data()
            user_data.update({'email': 'emmailemail.com'})
            serializer: UserSerializer = UserSerializer(data=user_data)
            serializer.is_valid(raise_exception=True)

    def test_if_username_error_show_expected_error_message(self) -> None:
        expected_error_message: str = 'Username must be at least 2 characters long'  # noqa: E501

        with self.assertRaisesMessage(
            serializers.ValidationError,
            expected_message=expected_error_message
        ):

            user_data: Dict[str, str] = self.get_user_data()
            user_data.update({'username': 'us'})
            serializer: UserSerializer = UserSerializer(data=user_data)
            serializer.is_valid(raise_exception=True)

    def test_if_email_error_show_expected_error_message(self) -> None:
        expected_error_message: str = 'Email must be a valid email address'

        with self.assertRaisesMessage(
            serializers.ValidationError,
            expected_message=expected_error_message
        ):

            user_data: Dict[str, str] = self.get_user_data()
            user_data.update({'email': 'emmailemail.com'})
            serializer: UserSerializer = UserSerializer(data=user_data)
            serializer.is_valid(raise_exception=True)
