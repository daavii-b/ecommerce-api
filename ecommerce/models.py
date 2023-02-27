from __future__ import annotations

import os
import string
from random import SystemRandom
from typing import Any, List, Tuple
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from PIL import Image


class Category(models.Model):
    id = models.UUIDField('id', default=uuid4, editable=False,
                          primary_key=True, unique=True)
    name = models.CharField('Name', max_length=120, unique=True)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name: str = 'Category'
        verbose_name_plural: str = 'Categories'


class Product(models.Model):
    id = models.UUIDField('id', default=uuid4, editable=False,
                          unique=True, primary_key=True)

    name = models.CharField('Product Name', max_length=255)
    slug = models.SlugField('Slug', unique=True, default='', blank=True)
    description = models.TextField('Product Description',
                                   blank=True, default='')
    stock = models.IntegerField('Stock', default=0, blank=True)
    cover = models.ImageField(
        'Cover',
        blank=True,
        default='',
        upload_to='images/'
    )

    price = models.FloatField('Price', default=0)
    promotional_price = models.FloatField('Promotional Price', default=0)

    created_at = models.DateTimeField('Created At', auto_now=True)
    updated_at = models.DateTimeField('Updated At', auto_now_add=True)

    on_sale = models.BooleanField('On sale', default=False)

    category = models.ForeignKey(
        Category,
        verbose_name='Category',
        on_delete=models.DO_NOTHING,
        default=None,
        null=True
    )

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self, *args, **kwargs) -> Any:

        random = SystemRandom()
        suffix: List[str] = random.choices(
            string.ascii_letters + string.digits, k=4
        )

        self.slug = slugify(self.name + '-' + str(suffix))

        save = super().save(*args, **kwargs)
        if self.cover:
            self.cover = self.resize_image(self.cover)
            return save

    @staticmethod
    def resize_image(image: Any, width: int = 300, height: int = 300):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)

        image_pillow = Image.open(image_full_path)

        original_image_size: Tuple[int, int] = image_pillow.size

        if original_image_size == (width, height):
            return image_pillow.close()

        new_image = image_pillow.resize(
            (width, height), Image.Resampling.LANCZOS
        )

        new_image.save(
            image_full_path,
            optimize=True,
            quality=60,
        )

        return new_image

    @staticmethod
    def stockless(product: Product) -> None:
        product.on_sale = False
        product.save()

    def clean(self, *args, **kwargs) -> None:

        self.stockless(self) if not getattr(self, 'stock') else ...

        return super().clean(*args, **kwargs)
