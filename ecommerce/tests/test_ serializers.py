from typing import Any, Dict

from rest_framework import serializers

from ..serializers import ProductSerializer
from .test_base import ProductBaseTestCase


class ProductSerializerTestCase(ProductBaseTestCase):

    def test_if_product_name_less_than_20_chars_raises_validation_error(self) -> None:  # noqa: E501
        # Ensure that the product serializer throws an exception
        # if the name is less than 20 chars

        with self.assertRaises(serializers.ValidationError):
            # Get the product data
            product_data: Dict[str, Any] = self.get_product_user_data()

            # Update the product name to an invalid value
            product_data.update({'name': 'Invalid Name'})

            # Serializing the product data
            serializer: ProductSerializer = ProductSerializer(
                data=product_data
            )
            # Checking if the serializer is valid
            serializer.is_valid(raise_exception=True)

    def test_if_product_price_less_than_0_raises_validation_error(self) -> None:  # noqa: E501
        # Ensure that the product serializer throws an exception
        # if the price is negative

        with self.assertRaises(serializers.ValidationError):
            # Get the product data
            product_data: Dict[str, Any] = self.get_product_user_data()
            # Set the price to an invalid value
            product_data.update({'price': -29})
            # Serializing the product data
            serializer: ProductSerializer = ProductSerializer(
                data=product_data
            )
            # Checking if the serializer is valid
            serializer.is_valid(raise_exception=True)

    def test_if_product_promotional_price_less_than_0_raises_validation_error(self) -> None:  # noqa: E501
        # Ensure that the product serializer throws an exception
        # if the promotional price is negative

        with self.assertRaises(serializers.ValidationError):
            # Get the product data
            product_data: Dict[str, Any] = self.get_product_user_data()
            # Set the price to an invalid value
            product_data.update({'promotional_price': -29})
            # Serializing the product data
            serializer: ProductSerializer = ProductSerializer(
                data=product_data
            )
            # Checking if the serializer is valid
            serializer.is_valid(raise_exception=True)

    def test_if_product_name_error_show_expected_error_message(self) -> None:  # noqa: E501
        # expected message if product name is invalid
        expected_error_message: str = 'Name must be at least 20 characters long'  # noqa: E501
        # Ensure that the product name error message is raised correctly
        with self.assertRaisesMessage(serializers.ValidationError, expected_message=expected_error_message):  # noqa: E501
            # Get the product data
            product_data: Dict[str, Any] = self.get_product_user_data()
            # Set the invalid value
            product_data.update({'name': -29})
            # Serializing the product data
            serializer: ProductSerializer = ProductSerializer(
                data=product_data
            )
            # Checking if the serializer is valid
            serializer.is_valid(raise_exception=True)

    def test_if_product_price_error_show_expected_error_message(self) -> None:  # noqa: E501
        # expected message if product price is invalid
        expected_error_message: str = 'Field price can`t be less than zero'
        # Ensure that the product price error message is raised correctly
        with self.assertRaisesMessage(serializers.ValidationError, expected_message=expected_error_message):  # noqa: E501
            # Get the product data
            product_data: Dict[str, Any] = self.get_product_user_data()
            # Set the invalid value
            product_data.update({'price': -29})
            # Serializing the product data
            serializer: ProductSerializer = ProductSerializer(
                data=product_data
            )
            # Checking if the serializer is valid
            serializer.is_valid(raise_exception=True)

    def test_if_product_promotional_price_error_show_expected_error_message(self) -> None:  # noqa: E501
        # expected message if product price is invalid
        expected_error_message: str = 'Field promotional price can`t be less than zero'  # noqa: E501
        # Ensure that the product price error message is raised correctly
        with self.assertRaisesMessage(serializers.ValidationError, expected_message=expected_error_message):  # noqa: E501
            # Get the product data
            product_data: Dict[str, Any] = self.get_product_user_data()
            #  Set the invalid value
            product_data.update({'promotional_price': -29})
            # Serializing the product data
            serializer: ProductSerializer = ProductSerializer(
                data=product_data
            )
            # Checking if the serializer is valid
            serializer.is_valid(raise_exception=True)
