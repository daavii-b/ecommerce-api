from typing import Any, Dict

from django.core.mail import get_connection
from django.test import TestCase

from ..services.email import UserEmailService


class UserServicesTestCase(TestCase):

    def get_email_data(
        self,
    ) -> Dict[str, Any]:
        return {
            'subject': 'Subject to tests purposes',
            'recipient_list': ['defaultEmailtotesters@gmail.com'],
            'fail_silently': False,
            'message': 'Message default to testers',
            'html_message': '<p>HTML message by default</p>',
            'connection': None,
        }

    def test_user_email_service_getters(self) -> None:
        email_data: Dict[str, Any] = self.get_email_data()
        email_service: UserEmailService = UserEmailService(**email_data)

        self.assertEqual(email_service.subject, email_data['subject'])
        self.assertEqual(email_service.message, email_data['message'])
        self.assertListEqual(
            email_service.recipient_list, email_data['recipient_list']
        )
        self.assertEqual(
            email_service.fail_silently, email_data['fail_silently']
        )
        self.assertEqual(
            email_service.html_message, email_data['html_message']
        )
        self.assertTrue(email_service.connection is not None)

    def test_email_service_setters(self) -> None:
        email_data: Dict[str, Any] = self.get_email_data()
        email_service: UserEmailService = UserEmailService(**email_data)

        email_service.subject = 'Other subject'
        email_service.message = 'Other message'
        email_service.recipient_list = ['otherEmailtoTester@email.com']
        email_service.fail_silently = True
        email_service.html_message = '<p>This is other message to test</p>'
        email_service.connection = get_connection()

        self.assertNotEqual(
            email_service.html_message, email_data['html_message']
        )
        self.assertNotEqual(
            email_service.fail_silently, email_data['fail_silently']
        )
        self.assertNotEqual(
            email_service.recipient_list, email_data['recipient_list']
        )
        self.assertNotEqual(email_service.connection, email_data['connection'])
        self.assertNotEqual(email_service.subject, email_data['subject'])
        self.assertNotEqual(email_service.message, email_data['message'])

    def test_email_service_validator(self) -> None:
        email_data: Dict[str, Any] = self.get_email_data()
        email_service: UserEmailService = UserEmailService(**email_data)

        list_with__invalid_emails = [
            'emailtoTester@email.com'
        ]

        email_service.recipient_list = list_with__invalid_emails

        self.assertTrue(email_service.is_valid())
