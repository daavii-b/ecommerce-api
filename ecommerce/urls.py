from rest_framework.routers import DefaultRouter

from .views import ProductView

app_name: str = 'ecommerce'

router = DefaultRouter()

router.register(r'products', ProductView, 'product')

urlpatterns = router.urls
