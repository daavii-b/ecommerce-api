import re


class EmailValidator:
    _email: str
    regex_email = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    )

    @classmethod
    def __init__(cls, email: str) -> None:
        cls._email = email

    @classmethod
    def is_valid(cls) -> bool:
        return True if cls.regex_email.fullmatch(cls._email) else False
