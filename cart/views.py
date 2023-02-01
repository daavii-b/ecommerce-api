# from datetime import timedelta
from typing import Any, Type

from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from users.models import User


class CartView(ViewSet):

    permission_classes: list[Type[IsAuthenticated]] = [IsAuthenticated,]

    @staticmethod
    def get_user_object(request) -> User | None:
        # Return an User object or None
        try:
            return User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_request_data(request) -> list:
        # Return an list with data from the request or an Empty list
        try:
            return request.data['productsCart']
        except KeyError:
            return []

    def list(self, request) -> Response:

        user_id: Any | str = getattr(self.get_user_object(request), 'id', '')

        if cache.get(user_id):
            return Response({
                "cart": cache.get(user_id),
            }, status=status.HTTP_200_OK)

        return Response({
            "cart": []
        }, status=status.HTTP_204_NO_CONTENT)

    def create(self, request) -> Response:

        # self.create_temporary_user_in_cache(request)

        # Define the key prefix
        cache.key_prefix = "cart"

        # Redis to work with json
        user_id: Any | str = getattr(
            self.get_user_object(request),
            'id', ''
        )

        # cache is the default cache backend, work with string.
        user_cart: Any = cache.get(user_id, None)

        # cart data sended from client-side
        data: list = self.get_request_data(request)

        # Create a new user cart if not already exists
        if user_cart is None:
            cache.set(user_id, data, timeout=None)
        else:
            # verify if have new product in the cart data
            if user_cart == data:
                return Response(data={
                    'cart': user_cart,
                })
            else:
                if not data:
                    # if products cart is empty, delete cached data
                    cache.delete(user_id)
                else:
                    # setting the new data in cache
                    cache.set(user_id, data, timeout=None)

        return Response(data={
            'cart': cache.get(user_id) or [],
        }, status=status.HTTP_200_OK)
