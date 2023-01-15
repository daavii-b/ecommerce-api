from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Product
from .serializers import ProductSerializer


class ProductView(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.filter(on_sale=True)
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    lookup_field = 'slug'
