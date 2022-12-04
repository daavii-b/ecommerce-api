from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'stock',
                  'created_at', 'updated_at']

    slug = serializers.SlugField(
        read_only=True
    )