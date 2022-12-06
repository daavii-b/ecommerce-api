from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import User
from .serializers import UserSerializer


class UserViewSet(ViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request) -> Response:
        data = request.data
        serializer = UserSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def partial_update(self, request) -> Response:
        return Response('Partial')

    def update(self, request) -> Response:
        return Response('Test')

    def destroy(self, request) -> Response:
        return Response('delete')
