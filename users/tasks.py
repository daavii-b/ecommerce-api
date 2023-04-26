from __future__ import absolute_import, unicode_literals

from typing import Union

from celery import shared_task
from celery.utils.log import get_task_logger

from utils.render import renders

from .models import User
from .services.email import UserEmailService

logger = get_task_logger(__name__)


def get_user_instance(user_email) -> Union[User, None]:
    try:
        return User.objects.get(email__exact=user_email)
    except User.DoesNotExist:
        return None


def get_email_service(
        domain: str, user: Union[User, None]) -> Union[UserEmailService, None]:
    if user:
        html_message: str = renders.email_render(domain, user)
        return UserEmailService(
            subject=f'Welcome to Ecommerce Project {user.username}!',
            recipient_list=[user.email],
            html_message=html_message,
        )
    return None


@shared_task(name="users.send_email_task")
def send_email_task(domain, user_email) -> None:
    email: UserEmailService = get_email_service(
        domain, get_user_instance(user_email)
    )

    if email is not None:
        logger.info('Sent confirmation email')

        email.send_email()
