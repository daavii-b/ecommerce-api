from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class EmailValidator:
    _email: str

    @classmethod
    def __init__(cls, email: str) -> None:
        cls._email = email

    @classmethod
    def is_valid(cls) -> bool:
        try:
            validate_email(cls._email)
        except ValidationError:
            return False
        return True
