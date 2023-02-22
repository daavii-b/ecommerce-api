from django.urls import reverse

from .test_base import AuthenticationBaseTestCase


class AuthenticationUrlsTestCase(AuthenticationBaseTestCase):

    def test_if_pair_tokens_url_is_corre(self) -> None:
        expected_url: str = '/api/tokens/'
        url: str = reverse('tokens:pair-tokens')

        self.assertEqual(url, expected_url)

    def test_the_test(self) -> None:
        expected_url: str = '/api/tokens/refresh/'
        url: str = reverse('tokens:refresh-token')

        self.assertEqual(url, expected_url)
