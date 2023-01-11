import string
from random import SystemRandom

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class EmailTokenGenerate(PasswordResetTokenGenerator):
    def __init__(self, *args, **kwargs) -> None:
        self.__random: SystemRandom = SystemRandom()
        super().__init__(*args, **kwargs)

    def __out_token(self) -> str:
        _out_token = self.__random.choices(
            string.ascii_letters + string.digits, k=6
        )

        return str(_out_token)

    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> str:
        return (
            text_type(user.pk) + text_type(timestamp) + text_type(
                self.__out_token()
            )
        )


token_email_generator: EmailTokenGenerate = EmailTokenGenerate()
