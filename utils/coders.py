from typing import Any

from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes
from django.utils.encoding import force_str as force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.response import Response


class Coders:

    def encode(self, data) -> str:
        return urlsafe_base64_encode(force_bytes(data))

    def decode(self, data) -> Any | None:
        try:
            decoded_data = force_text(urlsafe_base64_decode(data))

            return decoded_data
        except DjangoUnicodeDecodeError:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
