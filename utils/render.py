from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from utils.coders import Coders
from utils.tokens import token_email_generator


class Renders:

    __coder: Coders = Coders()

    @classmethod
    def email_render(cls, request, user) -> str:
        return render_to_string(
            'email/confirm_email.html',
            {
                'user': user,
                'domain': get_current_site(request),
                'uuid': cls.__coder.encode(user.pk),
                'token': token_email_generator.make_token(user)
            }
        )


renders = Renders()
