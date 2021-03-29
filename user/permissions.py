from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    message = 'Только Администратор имеет права на эти действия'

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin)


class IsAdminOrReadOnly(BasePermission):
    message = 'Только Администратор имеет права на эти действия'

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or (
                request.user.is_authenticated and request.user.is_admin))


class IsAuthorOrAdminOrModerator(BasePermission):
    message = ('Администратор, Автор или Модератор '
               'имеют права на эти действия')

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or (
                request.user and request.user.is_authenticated))

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or request.user.is_authenticated
                and (request.user.is_admin or request.user.is_moderator
                     or obj.author == request.user))
