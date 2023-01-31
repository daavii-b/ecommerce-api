import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Product


def delete_cover(instance: Product) -> None:
    try:
        os.remove(instance.cover.path)  # type: ignore
    except (ValueError, FileNotFoundError):
        pass


@receiver(pre_delete, sender=Product)
def product_cover_delete(sender, instance, *args, **kwargs) -> None:
    return delete_cover(instance)
