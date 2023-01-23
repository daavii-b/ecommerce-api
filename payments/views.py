import os
from typing import Any, Dict

import mercadopago
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from users.models import User

sdk = mercadopago.SDK(os.environ.get('MP_ACCESS_TOKEN'))


class PaymentsViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names: list[str] = [
        "post",
    ]

    @staticmethod
    def get_user(request) -> User | None:
        try:
            return User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            return None

    def get_payment_data(self, user, data) -> Dict[str, Any]:
        return {
            "additional_info": {
                "items": [
                    {
                        "id": "MLB2907679857",
                        "title": "Point Mini",
                        "description": "Producto Poin bluetooth",
                        "category_id": "electronics",
                        "unit_price": 58.8
                    }
                ],
                "payer": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone": {
                        "area_code": 11,
                        "number": 987654321,
                    },
                    "address": {},
                },
                "shipments": {
                    "receiver_address": {
                        "zip_code": '',
                        "state_name": '',
                        "city_name": '',
                        "street_name": '',
                        "street_number": '',
                    },
                },
            },
            "description": "Payment for product",
            "installments": int(data['installments']),
            "metadata": {},
            "payer": {
                "email": data['payer']['email'],
                "identification": data['payer']['identification'],
            },
            "token": data["token"],
            "issuer_id": data["issuer_id"],
            "transaction_amount": data["transaction_amount"],
            "payment_method_id": data["payment_method_id"],
        }

    def create(self, request) -> Response:
        payment_data: Dict[str, Any] = self.get_payment_data(
            self.get_user(request), request.data
        )
        payment = sdk.payment().create(payment_data)
        return Response(
            data=payment['response']['id'],
            status=status.HTTP_201_CREATED
        )
