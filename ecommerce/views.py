from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Product
from .serializers import ProductSerializer


class ProductView(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.filter(on_sale=True)
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    lookup_field: str = 'slug'
    http_method_names = ['get', 'post']

    @method_decorator(cache_page(
        60 * 12
    ))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
