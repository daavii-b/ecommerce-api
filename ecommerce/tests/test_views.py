from django.http import HttpResponse

from ecommerce.models import Product

from .test_base import ProductBaseTestCase


class ProductViewTestCase(ProductBaseTestCase):

    def test_if_product_list_returns_status_200(self) -> None:
        self.make_product_batch()

        response: HttpResponse = self.client.get(self.products_url)

        self.assertEqual(response.status_code, 200)

    def test_if_product_retrieve_return_status_200(self) -> None:
        product: Product = self.make_product()
        product_url: str = self.get_product_details_url(product.slug)

        response: HttpResponse = self.client.get(product_url)

        self.assertEqual(response.status_code, 200)
