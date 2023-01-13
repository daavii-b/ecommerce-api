from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from utils.coders import Coders
from utils.render import renders
from utils.tokens import token_email_generator

from .models import User
from .permissions import IsOwner, NewUser
from .serializers import UserSerializer
from .services.email import UserEmailService


class UserViewSet(ViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field: str = 'username'
    permission_classes = (NewUser, IsOwner,)
    http_method_names: list[str] = [
        "get", "post", "put", "patch", "delete", "options"
    ]
    coder = Coders()

    def get_email_service(self, request, user) -> UserEmailService:
        html_message: str = renders.email_render(request, user)
        return UserEmailService(
            'This a subject for testing purposes',
            [user.email],
            html_message=html_message,
        )

    def get_user(self, request) -> User:

        user: User = get_object_or_404(
            self.queryset,
            username=request.user.username
        )

        self.check_object_permissions(request, user)

        return user

    def retrieve(self, request) -> Response:
        user: User = get_object_or_404(
            self.queryset, username=request.user.username
        )

        serializer: UserSerializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request) -> Response:
        serializer: UserSerializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        email_service: UserEmailService = self.get_email_service(
            request, serializer.instance
        )

        email_service.send_email()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request) -> Response:
        user: User = self.get_user(request)

        serializer: UserSerializer = UserSerializer(
            partial=True,
            instance=user,
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request) -> Response:
        user: User = self.get_user(request)

        serializer: UserSerializer = UserSerializer(
            data=request.data,
            instance=user,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request) -> Response:
        user: User = self.get_user(request)

        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def confirm_email(request: HttpRequest, uuid: str, token: str):
    try:
        user_id: Any = UserViewSet.coder.decode(uuid)
        user: User = User.objects.get(pk=user_id)

        if token_email_generator.check_token(user, token):
            user.is_active = True
            user.save()

            return Response(status.HTTP_200_OK)
        else:
            raise AuthenticationFailed(
                detail='Your link to confirm your email address is invalid.',
                code=status.HTTP_401_UNAUTHORIZED,
            )

    except (ObjectDoesNotExist):
        raise NotFound(
            'User does not exist',
            status.HTTP_404_NOT_FOUND
        )
