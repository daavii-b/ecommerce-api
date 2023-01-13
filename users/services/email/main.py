from typing import Any, List

from django.conf import settings
from django.core.mail import get_connection, send_mail

from services.email import IEmailService
from validators import EmailValidator


class UserEmailService(IEmailService):

    def __init__(
        self, subject: str, recipient_list: List[str],
        fail_silently: bool = False, html_message: str = '',
        message: str = '', connection: Any = None,
    ) -> None:
        self.__from_email = settings.DEFAULT_FROM_EMAIL

        self._subject = subject
        self._message = message
        self._recipient_list = recipient_list
        self._fail_silently = fail_silently

        self._html_message = html_message

        self._connection: Any = connection if connection is not None \
            else get_connection(
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                fail_silently=self._fail_silently,
            )

    @property
    def subject(self) -> str:
        return self._subject

    @property
    def message(self) -> str:
        return self._message

    @property
    def recipient_list(self) -> List[str]:
        return self._recipient_list

    @property
    def fail_silently(self) -> bool:
        return self._fail_silently

    @property
    def html_message(self) -> str:
        return self._html_message

    @property
    def connection(self) -> str:
        return self._connection

    @subject.setter
    def subject(self, value: str) -> None:
        self._subject: str = value

    @message.setter
    def message(self, value: str) -> None:
        self._message: str = value

    @recipient_list.setter
    def recipient_list(self, value: List[str]) -> None:
        self._recipient_list: List[str] = value

    @fail_silently.setter
    def fail_silently(self, value: bool) -> None:
        self._fail_silently: bool = value

    @html_message.setter
    def html_message(self, value: str) -> None:
        self._html_message: str = value

    @connection.setter
    def connection(self, value: Any) -> None:
        self._connection = value

    def is_valid(self) -> bool:
        return all(
            [EmailValidator(email).is_valid()
                for email in self._recipient_list
             ]
        )

    def send_email(self) -> None:
        send_mail(
            from_email=self.__from_email,
            subject=self._subject,
            message=self._message,
            recipient_list=self._recipient_list,
            fail_silently=False,
            html_message=self._html_message,
            connection=self._connection
        )
