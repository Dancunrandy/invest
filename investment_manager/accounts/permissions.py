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
        if isinstance(obj, InvestmentAccount):
            account = obj
        elif isinstance(obj, Transaction):
            account = obj.account
        else:
            return False

        try:
            account_permission = AccountPermission.objects.get(user=request.user, account=account)
        except AccountPermission.DoesNotExist:
            return False

        return self.check_permission(account_permission.permission, request.method)

    def check_permission(self, permission, method):
        if permission == VIEW_PERMISSION:
            return method in permissions.SAFE_METHODS
        elif permission == CRUD_PERMISSION:
            return True
        elif permission == POST_PERMISSION:
            return method == 'POST'
        return False
