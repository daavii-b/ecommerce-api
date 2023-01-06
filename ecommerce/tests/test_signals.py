from django.test import override_settings
from PIL import Image

from .test_base import MEDIA_ROOT, ProductBaseTestCase


class ProductSignalsTestCase(ProductBaseTestCase):

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_if_product_was_deleted_cover_is_deleted(self) -> None:
        # Get an image for the product
        cover_path: str = self.get_image_file()
        # Create a product with the new image
        product = self.make_product(cover=cover_path)
        # Setting the product cover path
        product.cover.__setattr__('path', cover_path)  # type: ignore
        # Deleting the product
        product.delete()

        # Ensure that if the product was deleted then the cover is deleted
        with self.assertRaises(FileNotFoundError):
            Image.open(cover_path)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_if_product_do_not_have_cover_no_raises_error(self) -> None:
        # Create a product without an image file
        product = self.make_product(cover='')
        # Ensure that whether the product was deleted even without an image
        self.assertTrue(product.delete())
