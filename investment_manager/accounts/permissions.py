from rest_framework import permissions
from .models import AccountPermission, InvestmentAccount, Transaction

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

        if account_permission.permission == 'view':
            return request.method in permissions.SAFE_METHODS
        elif account_permission.permission == 'crud':
            return True
        elif account_permission.permission == 'post':
            return request.method == 'POST'

        return False
