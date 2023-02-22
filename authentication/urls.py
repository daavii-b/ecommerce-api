from django.urls import path

from .views import TokenPairViewSet, TokenRefreshViewSet

app_name = "tokens"

urlpatterns = [
    path(r'tokens/', TokenPairViewSet.as_view({
        "post": "create",
    }), name='pair-tokens'),
    path(r'tokens/refresh/', TokenRefreshViewSet.as_view({
        "post": "create",
    }), name='refresh-token'),
]
