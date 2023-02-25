
from django_filters.rest_framework import DjangoFilterBackend


class CategoryFilter(DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):
        category = request.query_params.get('category', None)

        if category:
            queryset = queryset.filter(
                category__name__icontains=category
            )

        return super().filter_queryset(request, queryset, view)
