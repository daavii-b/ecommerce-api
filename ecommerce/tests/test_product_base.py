import os
import shutil
from io import BytesIO
from typing import Any, Dict, Tuple

from django.conf import settings
from django.core.files.base import File
from django.test import TestCase
from PIL import Image

from ..models import Product

MEDIA_ROOT: str = os.path.join(settings.MEDIA_ROOT, 'tests/')


class ProductBaseTestCase(TestCase):
    def __init__(self, methodName) -> None:

        super().__init__(methodName)

    def tearDown(self) -> None:
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        return super().tearDown()

    @staticmethod
    def get_image_file(
        name: str = 'ImageForTest.png',
        ext: str = 'png',
        size: Tuple[int, int] = (500, 500),
        color: Tuple[int, int, int] = (255, 255, 255)
    ) -> File:
        file_obj: BytesIO = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    @staticmethod
    def make_product(
        name: str = 'My Product',
        description: str = 'Something about my product',
        stock: int = 12,
        price: float = 12.2,
        promotional_price: float = 12.1,
        on_sale: bool = True,
        cover: str | File = ''
    ) -> Product:
        return Product.objects.create(
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
        return os.path.join(MEDIA_ROOT, 'images', image_name)

    def get_product_user_data(self) -> Dict[str, Any]:
        return {
            'name': 'My Product must be an name greater than 20 chars',
            'description': 'Something about my product',
            'stock': 12,
            'price': 12.2,
            'promotional_price': 12.1,
            'on_sale': True,
            'cover': self.get_image_file(),
        }
