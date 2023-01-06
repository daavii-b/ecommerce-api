from typing import Tuple

from django.test import override_settings
from PIL import Image

from ..models import Product
from .test_base import MEDIA_ROOT, ProductBaseTestCase


class ProductModelTestCase(ProductBaseTestCase):

    def test_if_str_method_returns_the_product_name(self) -> None:
        # Expected Product Name
        product_name: str = 'MyProductName'.capitalize()

        # Make a Product with the expected name
        product: Product = self.make_product(name=product_name)

        # Product str representation must match the expected name
        self.assertEqual(str(product), product_name)

    def test_if_product_do_not_have_stock_on_sale_must_be_false(self) -> None:
        # Make a Product without stock
        product = self.make_product(stock=0)

        # if product don`t have stock, on sale must be set to False
        product.clean()

        # Ensure that on sale is set to False
        self.assertFalse(product.on_sale)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_if_product_cover_is_resizing_to_300_px(self) -> None:
        # Image size
        cover_size: Tuple[int, int] = (400, 600)

        # Product Image Path
        cover_path: str = self.get_image_file(
            name='Image.jpg', size=cover_size
        )

        #  Make the Product
        self.make_product(cover=cover_path)

        # Product Image size that was saved
        final_cover_size: Tuple[int, int] = Image.open(cover_path).size

        # The cover size must be 300x300 pixels
        expected_cover_size: Tuple[int, int] = (300, 300)

        # Ensure that the product image is resized to 300 pixels
        self.assertEqual(final_cover_size, expected_cover_size)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_product_width_do_not_need_to_be_resized(self) -> None:
        # The Image size is resized to 300 pixels when the product is saved.
        size: Tuple[int, int] = (300, 300)

        # The Product Image Path
        cover_path: str = self.get_image_file(
            name='ImageForTest.png',
            size=size
        )

        # The Product Image don`t need to be resized
        self.make_product(cover=cover_path)

        # Get the Image size
        cover_size: Tuple[int, int] = Image.open(cover_path).size

        self.assertEqual(cover_size, size)
