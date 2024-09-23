from rest_framework import permissions
from .models import AccountPermission, InvestmentAccount, Transaction

# Define permission constants
VIEW_PERMISSION = 'view'
CRUD_PERMISSION = 'crud'
POST_PERMISSION = 'post'

class HasAccountPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the object based on AccountPermission.
        """
        account = obj.account if isinstance(obj, Transaction) else obj
        
        try:
            account_permission = AccountPermission.objects.get(user=request.user, account=account)
        except AccountPermission.DoesNotExist:
            return False

        return self.check_permission(account_permission.permission, request.method)

    def check_permission(self, permission, method):
        permission_map = {
            VIEW_PERMISSION: permissions.SAFE_METHODS,
            CRUD_PERMISSION: True,
            POST_PERMISSION: ['POST']
        }
        
        allowed_methods = permission_map.get(permission, [])
        if permission == VIEW_PERMISSION:
            return method in allowed_methods
        elif permission == CRUD_PERMISSION:
            return True
        elif permission == POST_PERMISSION:
            return method in allowed_methods
        
        return False
