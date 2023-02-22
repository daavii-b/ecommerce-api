import os
import shutil
from typing import Any, Dict, Tuple

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from ..models import Product

MEDIA_ROOT: str = os.path.join(settings.MEDIA_ROOT, 'tests/images/')


class ProductBaseTestCase(TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        self.products_url: str = reverse('ecommerce:products-list')

        return super().__init__(methodName)

    def setUp(self) -> None:
        try:
            # Create the media directory for the tests
            os.makedirs(MEDIA_ROOT)
        except (FileExistsError, FileNotFoundError):
            ...
        return super().setUp()

    def tearDown(self) -> None:
        # Remove the media directory
        shutil.rmtree(
            os.path.join(settings.MEDIA_ROOT, 'tests/'),
            ignore_errors=True
        )
        return super().tearDown()

    def get_image_file(
        self,
        name: str = 'ImageForTest.png',
        ext: str = 'png',
        size: Tuple[int, int] = (500, 500),
    ) -> str:
        """
        get_image_file creates an image file

        Creates an image file an save it to the media directory and
        returns the path to the image file

        :param name: Name of the image file, defaults to 'ImageForTest.png'
        :type name: str, optional
        :param ext: Image extension, defaults to 'png'
        :type ext: str, optional
        :param size: Image width and height, defaults to (500, 500)
        :type size: Tuple[int, int], optional
        :return: Return the path to the image file
        :rtype: str
        """

        image = Image.new('RGB', size=size)
        image_path = self.get_image_full_path(name)
        image.save(
            image_path, ext, optimize=True, path=image_path, name=name
        )
        return image_path

    @staticmethod
    def make_product(
        name: str = 'My Product',
        description: str = 'Something about my product',
        stock: int = 12,
        price: float = 12.2,
        promotional_price: float = 12.1,
        on_sale: bool = True,
        cover: str = ''
    ) -> Product:
        """
        make_product Makes an product

        Makes an Product object based on the parameters and
        returns the Product instance

        :param name: Name of the product, defaults to 'My Product'
        :type name: str, optional
        :param description: Description of the product,
            defaults to 'Something about my product'
        :type description: str, optional
        :param stock: Quantity of product in the available, defaults to 12
        :type stock: int, optional
        :param price: An price to the product, defaults to 12.2
        :type price: float, optional
        :param promotional_price:
            An promotional price to the product, defaults to 12.1
        :type promotional_price: float, optional
        :param on_sale: Show if the product is on sale, defaults to True
        :type on_sale: bool, optional
        :param cover: Image of the product, defaults to ''
        :type cover: str, optional
        :return: An product instance
        :rtype: Product
        """

        return Product.objects.create(
            name=name,
            description=description,
            stock=stock,
            price=price,
            promotional_price=promotional_price,
            on_sale=on_sale,
            cover=cover
        )

    def make_product_batch(self, quantity: int = 10) -> None:
        for index in range(quantity):
            name: str = f'My Produc {index}'
            description: str = 'Something about my product'
            stock: int = 12
            price: float = 12.2
            promotional_price: float = 12.1
            on_sale: bool = True
            cover: str = ''

            Product.objects.create(
                name=name,
                description=description,
                stock=stock,
                price=price,
                promotional_price=promotional_price,
                on_sale=on_sale,
                cover=cover
            )

    @staticmethod
    def get_image_full_path(image_name: str) -> str:
        """Return an Image full path"""
        return os.path.join(MEDIA_ROOT, image_name)

    def get_product_user_data(self) -> Dict[str, Any]:
        """
        get_product_user_data makes an dict with product raw data

        Makes an dict that contains an product raw data and return it

        :return: An dict with product data
        :rtype: Dict[str, Any]
        """

        return {
            'name': 'My Product must be an name greater than 20 chars',
            'description': 'Something about my product',
            'stock': 12,
            'price': 12.2,
            'promotional_price': 12.1,
            'on_sale': True,
            'cover': self.get_image_file(),
        }

    @staticmethod
    def get_product_details_url(product_slug: str) -> str:
        return reverse(
            'ecommerce:products-detail',
            kwargs={'slug': product_slug}
        )
