
from django.urls import path

from .views import PaymentsViewSet

urlpatterns = [
    path(r'payments/', PaymentsViewSet.as_view(
        {'post': 'create', }
    ), name='payments')
]
