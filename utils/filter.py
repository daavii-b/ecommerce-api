
from django.db.models import Q
from django_filters import rest_framework as filters

from ecommerce.models import Product


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte', )

    min_promotional_price = filters.NumberFilter(
        field_name='promotional_price',
        lookup_expr='gte',
    )
    max_promotional_price = filters.NumberFilter(
        field_name='promotional_price',
        method='filter_max_promotional_price'
    )

    category = filters.CharFilter(
        field_name='category__name',
        lookup_expr='iexact'
    )

    range = filters.RangeFilter()

    def filter_max_promotional_price(self, queryset, name, value) -> None:
        return queryset.filter(
            Q(promotional_price__gt=0) & Q(promotional_price__lte=value)
        )

    class Meta:
        model = Product
        fields = ['category', 'price', 'promotional_price']
