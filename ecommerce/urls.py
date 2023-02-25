from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryView, ProductView

app_name: str = 'ecommerce'

router = DefaultRouter()

router.register(r'products', ProductView, 'products')
router.register(r'categories', CategoryView, 'categories')

urlpatterns = [
    path('', include(router.urls)),
]
