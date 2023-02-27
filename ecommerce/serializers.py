from collections import defaultdict

from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs) -> None:
        self._errors: defaultdict[str, list] = defaultdict(list)
        self._field: str = ''
        return super().__init__(*args, **kwargs)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'cover', 'price',
            'promotional_price', 'stock', 'category', 'category_name',
            'created_at', 'updated_at'
        ]

    slug = serializers.SlugField(
        read_only=True
    )

    category = serializers.HyperlinkedRelatedField(
        view_name='ecommerce:categories-detail', read_only=True,
        lookup_field='name'
    )

    category_name = serializers.StringRelatedField(
        read_only=True,
        source='category'
    )

    def validate_name(self, value) -> str:
        self._field = 'name'
        if len(value) < 20:
            self._errors[self._field].append(
                'Name must be at least 20 characters long'
            )

        if self._errors[self._field]:
            raise serializers.ValidationError(self._errors[self._field])

        return value

    def validate_price(self, value) -> float:
        self._field = 'price'

        if value < 0:
            self._errors[self._field].append(
                'Field price can`t be less than zero'
            )

        if self._errors[self._field]:
            raise serializers.ValidationError(self._errors[self._field])

        return value

    def validate_promotional_price(self, value) -> float:
        self._field = 'promotional_price'

        if value < 0:
            self._errors[self._field].append(
                'Field promotional price can`t be less than zero'
            )

        if self._errors[self._field]:
            raise serializers.ValidationError(self._errors[self._field])

        return value
