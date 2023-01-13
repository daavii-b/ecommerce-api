from django.urls import path

from . import views

app_name: str = 'users'


urlpatterns = [
    path(
        r'users/confirm_email/<uuid>/<token>',
        views.confirm_email, name='confirm_email'
    ),
    path(
        r'users/', views.UserViewSet.as_view({
            'get': 'retrieve',
            'post': 'create',
            'delete': 'destroy',
            'put': 'update',
            'patch': 'partial_update',
        }),
        name='users'
    ),
]
