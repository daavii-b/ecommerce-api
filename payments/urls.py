from django.urls import path

from . import views

urlpatterns = [
    path(
        r'create-checkout-session/',
        views.CheckoutSessionView.as_view(),
        name="create-checkout-session"
    ),

    path(
        r'create-payment-intent/',
        views.CreatePaymentIntentView.as_view(), name="create-payment-intent"
    )
]
