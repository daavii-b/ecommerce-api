from typing import List

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken


class TokenPairViewSet(ViewSet):

    http_method_names: List[str] = ['post']

    def create(self, request) -> Response:
        user = authenticate(
            request,
            email=request.data['email'],
            password=request.data['password']
        )
        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK
            )

        return Response({
            'detail': 'Credentials is invalid.',
        }, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshViewSet(ViewSet):

    http_method_names: List[str] = ['post']

    def create(self, request) -> Response:
        try:
            refresh_token: str = request.data['refresh']

            token: RefreshToken = RefreshToken(refresh_token, verify=True)

            return Response({
                "access": str(token.access_token),
                "refresh": str(token)
            }, status=200)

        except KeyError:
            return Response({
                "error": "Parameter 'refresh' is missing from the request data"
            }, status=status.HTTP_400_BAD_REQUEST)
