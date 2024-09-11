from rest_framework import permissions
from .models import AccountPermission

class HasAccountPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            account_permission = AccountPermission.objects.get(user=request.user, account=obj)
        except AccountPermission.DoesNotExist:
            return False

        if account_permission.permission == 'view':
            return request.method in permissions.SAFE_METHODS  
        elif account_permission.permission == 'crud':
            return True  
        elif account_permission.permission == 'post':
            return request.method == 'POST'  

        return False
