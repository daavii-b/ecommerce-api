from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse

from utils.coders import Coders
from utils.tokens import token_email_generator


class Renders:

    __coder: Coders = Coders()

    @classmethod
    def get_user_email_url(cls, user) -> str:
        return reverse('users:confirm_email', args=(
            cls.__coder.encode(user.pk),
            token_email_generator.make_token(user)
        ))

    @classmethod
    def email_render(cls, request, user) -> str:
        url: str = cls.get_user_email_url(user)

        return render_to_string(
            'email/confirm_email.html',
            {
                'user': user,
                'domain': get_current_site(request),
                'url': url,
            }
        )


renders = Renders()
