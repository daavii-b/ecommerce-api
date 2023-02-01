from typing import Any

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from users.tasks import send_email_task
from utils.coders import Coders
from utils.tokens import token_email_generator

from .models import User
from .permissions import IsOwner, NewUser
from .serializers import UserSerializer


class UserViewSet(ViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field: str = 'username'
    permission_classes = (NewUser, IsOwner,)
    http_method_names: list[str] = [
        "get", "post", "put", "patch", "delete", "options"
    ]
    coder: Coders = Coders()

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

        send_email_task.delay(
            domain=str(get_current_site(request)),
            user_email=serializer.data['email'],
        )  # type: ignore

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
def confirm_email(request: HttpRequest, uuid: str, token: str) -> Response:
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

    except User.DoesNotExist:
        raise NotFound(
            'User does not exist',
            code=status.HTTP_404_NOT_FOUND
        )


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def resend_confirmation_email(request: HttpRequest, username: str) -> Response:
    try:
        user: User = User.objects.get(
            username__exact=username
        )

        send_email_task.delay(
            domain=str(get_current_site(request)),
            user_email=user.email,
        )  # type: ignore

        return Response(status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
