from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductView

app_name: str = 'ecommerce'

router = DefaultRouter()

router.register(r'products', ProductView, 'product')

urlpatterns = [
    path('', include(router.urls)),
]
