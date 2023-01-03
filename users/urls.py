from django.urls import path

from .views import UserViewSet

app_name: str = 'users'

urlpatterns = [
    path(
        r'users/', UserViewSet.as_view({
            'get': 'retrieve',
            'post': 'create',
            'delete': 'destroy',
            'put': 'update',
            'patch': 'partial_update',
        }),
        name='users'
    ),
]
