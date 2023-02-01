from django.urls import path

from .views import CartView

urlpatterns = [
    path(r'cart/', CartView.as_view({
        "get": "list",
        "post": "create",

    })),
]
