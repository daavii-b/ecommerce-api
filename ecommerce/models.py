from typing import Any
from uuid import uuid4

from django.db import models


class Product(models.Model):
    id = models.UUIDField('id', default=uuid4, editable=False,
                          unique=True, primary_key=True)

    name = models.CharField('Product Name', max_length=255)
    slug = models.SlugField('Slug', unique=True,)
    description = models.TextField('Product Description',
                                   blank=True, default='')
    inventory = models.IntegerField('Inventory', default=0, blank=True)

    created_at = models.DateTimeField('Created At', auto_now=True)
    updated_at = models.DateTimeField('Updated At', auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self, *args, **kwargs) -> Any:

        return super().save(*args, **kwargs)
