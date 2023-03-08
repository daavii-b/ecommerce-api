
import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# This is your test secret API key.
stripe.api_key = 'sk_test_51MRQc9ILB47AslaJsNm0Xm7TCKCr9hnaNpMFRD34HwlXOAGjL9wmuEOkxgdbSlTT9p4brD86sV7Nb3etGpVAXy0o00O9DRuMcJ'  # noqa: E501


class CheckoutSessionView(CreateAPIView):
    # permission_classes = [IsAuthenticated]

    @staticmethod
    def get_products_list(request):
        return [
            {
                'price_data': {
                    'unit_amount_decimal':
                        (
                            item['product']['promotional_price'] or
                            item['product']['price']
                        ) * 100,
                    'currency': 'brl',
                    'product_data': {
                        'name': item['product']['name'],
                        'images': [item['product']['cover'],],
                        'metadata': {
                            'product_id': item['product']['id'],
                            'description': item['product']['description'],
                        }
                            },
                },
                'quantity': item['qty']

            } for item in request.data.get('products')
        ]

    def post(self, request, *args, **kwargs):

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card',],
                customer_email="useremail1@gmail.com",
                submit_type="pay",
                line_items=self.get_products_list(request),
                mode='payment',
                currency='brl',
                success_url=settings.SITE_URL +
                '/payments/status/?success=true',
                cancel_url=settings.SITE_URL +
                '/payments/status/?canceled=true',
            )
        except Exception as e:
            print(str(e))
            return Response({
                'error':
                    'An error occurred while creating the checkout session',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {'checkout_url': checkout_session.url},
            status=status.HTTP_200_OK
        )


class CreatePaymentIntentView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        try:

            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=1200,
                currency='brl',
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return Response({
                'clientSecret': intent['client_secret']
            }, status=200)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=500)
