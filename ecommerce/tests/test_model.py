from typing import Tuple

from django.core.files.base import File
from django.test import override_settings
from PIL import Image

from ..models import Product
from .test_product_base import MEDIA_ROOT, ProductBaseTestCase


class ProductModelTestCase(ProductBaseTestCase):

    def test_if_str_method_returns_the_product_name(self) -> None:
        # Expected Product Name
        product_name: str = 'MyProductName'.capitalize()

        # Make a Product with the expected name
        product: Product = self.make_product(name=product_name)

        # Product str representation must match the expected name
        self.assertEqual(str(product), product_name)

    def test_if_product_do_not_have_stock_on_sale_must_be_false(self) -> None:
        # Make a Product with no stock
        product = self.make_product(stock=0)

        # Product with no stock must have on sale set to False
        product.clean()

        # Ensure that the product has no stock on sale been set to False
        self.assertFalse(product.on_sale)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_if_product_cover_is_resizing_to_300_px(self) -> None:
        # The default cover size is 500x500
        cover: File = self.get_image_file()

        #  Make the Product
        self.make_product(cover=cover)

        # The Product Image Path
        cover_path: str = self.get_image_full_path(cover.name)

        # Get the Image size
        cover_size: Tuple[int, int] = Image.open(cover_path).size

        # The expected cover size must be 300x300 pixels
        expected_cover_size: Tuple[int, int] = (300, 300)

        # Ensure that the product image is resized to 300 pixels
        self.assertEqual(cover_size, expected_cover_size)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_product_width_do_not_need_to_be_resized(self) -> None:
        # The Image size is resized to 300 pixels when the product is saved.
        size: Tuple[int, int] = (300, 300)

        cover: File = self.get_image_file(
            name='ImageForTest.png',
            size=size
        )

        # The Product Image don`t need to be resized
        self.make_product(cover=cover)

        # The Product Image Path
        cover_path: str = self.get_image_full_path(cover.name)

        # Get the Image size
        cover_size: Tuple[int, int] = Image.open(cover_path).size

        self.assertEqual(cover_size, size)
