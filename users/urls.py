from django.urls import path

from .views import UserViewSet

urlpatterns = [
    path(
        r'users', UserViewSet.as_view({
            'post': 'create',
            'delete': 'destroy',
            'put': 'update',
            'patch': 'partial_update',
        }),
        name='users'
    ),
]
