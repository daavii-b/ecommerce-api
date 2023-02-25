
import os

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from utils.filter import CategoryFilter

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryView(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    lookup_field: str = 'name'
    http_method_names = ['get',]

    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset.order_by('name'))


class ProductPagination(PageNumberPagination):

    page_size: int = int(os.environ.get('PAGE_SIZE', 12))


class ProductView(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.filter(on_sale=True).select_related('category')
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = ProductPagination
    lookup_field: str = 'slug'
    http_method_names = ['get', 'post']

    filter_backends = [filters.SearchFilter, CategoryFilter]

    search_fields: list[str] = ["$name", "$price", "$promotional_price"]
    filterset_fields = ['category__name']

    # @method_decorator(cache_page(60*10, key_prefix='home_page'))
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60*10, key_prefix='detail_product'))
    def retrieve(self, request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset.order_by('-created_at'))
