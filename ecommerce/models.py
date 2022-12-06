from __future__ import annotations

import string
from random import SystemRandom
from typing import Any
from uuid import uuid4

from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    id = models.UUIDField('id', default=uuid4, editable=False,
                          unique=True, primary_key=True)

    name = models.CharField('Product Name', max_length=255)
    slug = models.SlugField('Slug', unique=True, default='', blank=True)
    description = models.TextField('Product Description',
                                   blank=True, default='')
    stock = models.IntegerField('Stock', default=0, blank=True)

    price = models.FloatField('Price', default=0)
    promotional_price = models.FloatField('Promotional Price', default=0)

    created_at = models.DateTimeField('Created At', auto_now=True)
    updated_at = models.DateTimeField('Updated At', auto_now_add=True)

    on_sale = models.BooleanField('On sale', default=False)

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self, *args, **kwargs) -> Any:
        self.name = self.name.capitalize()

        random = SystemRandom()
        suffix = random.choices(
            string.ascii_letters + string.digits, k=4
        )

        self.slug = slugify(self.name + '-' + str(suffix))

        return super().save(*args, **kwargs)

    @staticmethod
    def stockless(product: Product) -> None:
        product.on_sale = False
        product.save()

    def clean(self, *args, **kwargs) -> Any:

        if not getattr(self, 'stock'):
            self.stockless(self)

        return super().clean(*args, **kwargs)
