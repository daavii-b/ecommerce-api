from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField('id', default=uuid4, editable=False,
                          unique=True, primary_key=True)
    email = models.EmailField('E-mail', unique=True)

    is_active = models.BooleanField(
        "active",
        default=False,
        help_text="Designates whether this user should be treated as active."
        "Unselect this instead of deleting accounts.",
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return f'{self.username}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'users'
