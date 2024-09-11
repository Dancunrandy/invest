from django.test import TestCase
from django.contrib.auth.models import User
from .models import InvestmentAccount, AccountPermission, Transaction

class InvestmentAccountTestCase(TestCase):
    def setUp(self):
        # Create a user and an investment account for testing
        self.user = User.objects.create(username='testuser', password='password')
        self.account = InvestmentAccount.objects.create(name='Test Account')
        AccountPermission.objects.create(user=self.user, account=self.account, permission='crud')

    def test_account_creation(self):
        """Test if an investment account is created successfully."""
        account = InvestmentAccount.objects.get(name='Test Account')
        self.assertEqual(account.name, 'Test Account')

    def test_user_permission(self):
        """Test if a user has correct permissions."""
        permission = AccountPermission.objects.get(user=self.user, account=self.account)
        self.assertEqual(permission.permission, 'crud')

    def test_transaction_creation(self):
        """Test creating a transaction."""
        transaction = Transaction.objects.create(account=self.account, user=self.user, amount=100.00)
        self.assertEqual(transaction.amount, 100.00)
