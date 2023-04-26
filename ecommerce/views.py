
import os
from collections import OrderedDict
from typing import List

# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from utils.filter import ProductFilter

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryView(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    lookup_field: str = 'name'
    http_method_names = ['get', ]

    def list(self, request, *args, **kwargs) -> Response:
        serializer: CategorySerializer = CategorySerializer(
            self.get_queryset(),
            many=True
        )

        return Response(
            {'count': len(serializer.data), 'results': serializer.data, },
            status=status.HTTP_200_OK
        )

    def get_queryset(self):
        queryset = self.queryset.order_by('name')

        return queryset

    def retrieve(self, request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset.order_by('name'))


class ProductPagination(PageNumberPagination):

    page_size: int = int(os.environ.get('PAGE_SIZE', 20))

    def paginate_queryset(self, queryset, request, view=None):
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request
                                          })

        self.queryset = serializer.data

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):

        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('products', self.queryset)
        ]))


class ProductView(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.filter(
        on_sale=True
    ).select_related('category')
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    pagination_class = ProductPagination
    lookup_field: str = 'slug'
    http_method_names: List[str] = ['get', 'post']

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]

    search_fields: List[str] = ["$name", "$price", "$promotional_price"]
    filterset_class = ProductFilter
    # filterset_fields = ['category__name', 'price', 'promotional_price']

    # @method_decorator(cache_page(60*10, key_prefix='home_page'))
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    # @method_decorator(cache_page(60*10, key_prefix='detail_product'))
    def retrieve(self, request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset.order_by('-created_at'))
