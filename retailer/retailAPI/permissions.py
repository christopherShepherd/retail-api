from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists()


class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        if (request.user.groups.filter(name='delivery-crew').exists()
            and ([*request.data.keys()] == ['status'])):
            return True
        else:
            return False