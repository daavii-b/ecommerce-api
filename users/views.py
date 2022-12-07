from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import User
from .permissions import IsOwner, NewUser
from .serializers import UserSerializer


class UserViewSet(ViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (NewUser, IsOwner)

    def get_user(self, request) -> User:

        user = get_object_or_404(
            self.queryset,
            username=request.user.username
        )

        self.check_object_permissions(request, user)

        return user

    def create(self, request) -> Response:
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request) -> Response:
        user = self.get_user(request)

        serializer = UserSerializer(
            partial=True,
            instance=user,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request) -> Response:
        user = self.get_user(request)

        serializer = UserSerializer(
            instance=user,
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request) -> Response:
        user = self.get_user(request)

        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
