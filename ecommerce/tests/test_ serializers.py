from typing import Any, Dict

from rest_framework import serializers

from ..serializers import ProductSerializer
from .test_product_base import ProductBaseTestCase


class ProductSerializerTestCase(ProductBaseTestCase):

    def test_if_product_name_less_than_20_chars_raises_validation_error(self) -> None:  # noqa: E501

        with self.assertRaises(serializers.ValidationError):
            product_data: Dict[str, Any] = self.get_product_user_data()
            product_data.update({'name': 'Invalid Name'})

            serializer: ProductSerializer = ProductSerializer(
                data=product_data
            )

            serializer.is_valid(raise_exception=True)

    def test_if_product_price_less_than_0_raises_validation_error(self) -> None:  # noqa: E501

        with self.assertRaises(serializers.ValidationError):
            product_data: Dict[str, Any] = self.get_product_user_data()
            product_data.update({'price': -29})

            serializer: ProductSerializer = ProductSerializer(
                data=product_data
            )

            serializer.is_valid(raise_exception=True)

    def test_if_product_promotional_price_less_than_0_raises_validation_error(self) -> None:  # noqa: E501

        with self.assertRaises(serializers.ValidationError):
            product_data: Dict[str, Any] = self.get_product_user_data()
            product_data.update({'promotional_price': -29})

            serializer: ProductSerializer = ProductSerializer(
                data=product_data
            )

            serializer.is_valid(raise_exception=True)

    def test_if_product_name_error_show_expected_error_message(self) -> None:  # noqa: E501
        expected_error_message: str = 'Name must be at least 20 characters long'  # noqa: E501

        with self.assertRaisesMessage(serializers.ValidationError, expected_message=expected_error_message):  # noqa: E501
            product_data: Dict[str, Any] = self.get_product_user_data()
            product_data.update({'name': -29})

            serializer: ProductSerializer = ProductSerializer(
                data=product_data
            )

            serializer.is_valid(raise_exception=True)

    def test_if_product_price_error_show_expected_error_message(self) -> None:  # noqa: E501
        expected_error_message: str = 'Field price can`t be less than zero'

        with self.assertRaisesMessage(serializers.ValidationError, expected_message=expected_error_message):  # noqa: E501
            product_data: Dict[str, Any] = self.get_product_user_data()
            product_data.update({'price': -29})

            serializer: ProductSerializer = ProductSerializer(
                data=product_data
            )

            serializer.is_valid(raise_exception=True)

    def test_if_product_promotional_price_error_show_expected_error_message(self) -> None:  # noqa: E501
        expected_error_message: str = 'Field promotional price can`t be less than zero'  # noqa: E501

        with self.assertRaisesMessage(serializers.ValidationError, expected_message=expected_error_message):  # noqa: E501
            product_data: Dict[str, Any] = self.get_product_user_data()
            product_data.update({'promotional_price': -29})

            serializer: ProductSerializer = ProductSerializer(
                data=product_data
            )

            serializer.is_valid(raise_exception=True)
