from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

from utils.render import renders

from .models import User
from .services.email import UserEmailService

logger = get_task_logger(__name__)


def get_user_instance(user_email) -> User:
    return User.objects.get(email__exact=user_email)


def get_email_service(domain: str, user: User) -> UserEmailService:
    html_message: str = renders.email_render(domain, user)
    return UserEmailService(
        'This email is sent through celery and rabbitMQ.',
        [user.email],
        html_message=html_message,
    )


@shared_task(name="users.send_email_task")
def send_email_task(domain, user_email) -> None:
    email: UserEmailService = get_email_service(
        domain, get_user_instance(user_email)
    )

    logger.info('Sent confirmation email')

    email.send_email()
