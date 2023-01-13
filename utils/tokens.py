from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class EmailTokenGenerate(PasswordResetTokenGenerator):

    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> str:
        return (text_type(user.pk) + text_type(timestamp))


token_email_generator: EmailTokenGenerate = EmailTokenGenerate()
