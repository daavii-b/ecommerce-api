from rest_framework.permissions import BasePermission

NEW_USER_SAFE_METHODS = (
    'POST', 'OPTIONS', 'HEAD'
)


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return obj.username == request.user.username

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class NewUser(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return not (
            request.user.is_authenticated and request.method
            in NEW_USER_SAFE_METHODS
        )
