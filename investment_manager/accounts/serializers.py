from rest_framework import serializers
from .models import InvestmentAccount, AccountPermission, Transaction
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class AccountPermissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AccountPermission
        fields = ['user', 'permission']

class InvestmentAccountSerializer(serializers.ModelSerializer):
    permissions = AccountPermissionSerializer(source='accountpermission_set', many=True, read_only=True)

    class Meta:
        model = InvestmentAccount
        fields = ['id', 'name', 'permissions']

class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'account', 'user', 'amount', 'timestamp']
