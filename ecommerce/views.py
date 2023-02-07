from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
