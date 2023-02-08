
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


class ProductView(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.filter(on_sale=True)
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    lookup_field: str = 'slug'
    http_method_names = ['get', 'post']

    filter_backends = [filters.SearchFilter]
    search_fields: list[str] = ["name", "price", "promotional_price"]
    # filterset_fields = ['category', 'in_stock']

    @method_decorator(cache_page(60*10, key_prefix='home_page'))
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60*10, key_prefix='detail_product'))
    def retrieve(self, request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)
