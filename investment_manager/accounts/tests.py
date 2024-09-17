from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import InvestmentAccount, Transaction, AccountPermission
from django.test import TestCase

class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='password')
        self.account = InvestmentAccount.objects.create(name='Test Account')
        AccountPermission.objects.create(user=self.user, account=self.account, permission='crud')
        self.transaction = Transaction.objects.create(account=self.account, user=self.user, amount=100.00)
    
    def authenticate_user(self, username, password):
        self.client.login(username=username, password=password)
    
    def logout_user(self):
        self.client.logout()

class UserPermissionsTests(APITestCase):
    
    def setUp(self):
        super().setUp()  
        
        self.user = User.objects.create_user(username='user', password='password')
        self.admin = User.objects.create_superuser(username='admin', password='password')

        self.client.login(username='user', password='password')

        self.account1 = InvestmentAccount.objects.create(name='View Only Account')
        self.account2 = InvestmentAccount.objects.create(name='CRUD Account')
        self.account3 = InvestmentAccount.objects.create(name='Post Only Account')

        AccountPermission.objects.create(user=self.user, account=self.account1, permission='view')
        AccountPermission.objects.create(user=self.user, account=self.account2, permission='crud')
        AccountPermission.objects.create(user=self.user, account=self.account3, permission='post')

        self.transaction1 = Transaction.objects.create(user=self.user, account=self.account2, amount=100)
        self.transaction2 = Transaction.objects.create(user=self.user, account=self.account3, amount=200)
        self.transaction3 = Transaction.objects.create(user=self.user, account=self.account2, amount=300, timestamp='2024-01-01T00:00:00Z')
        self.transaction4 = Transaction.objects.create(user=self.user, account=self.account2, amount=400, timestamp='2024-02-01T00:00:00Z')

    def test_user_with_view_permission_cannot_create_transaction(self):
        self.authenticate_user('user', 'password')
        response = self.client.post('/transactions/', {'account': self.account1.id, 'amount': 500})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_with_crud_permission_can_create_transaction(self):
        self.authenticate_user('user', 'password')
        response = self.client.post('/transactions/', {'account': self.account2.id, 'amount': 500})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_with_post_only_permission_cannot_view_transactions(self):
        self.authenticate_user('user', 'password')
        response = self.client.get(f'/transactions/{self.transaction2.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_access_all_transactions(self):
        self.logout_user()
        self.authenticate_user('admin', 'password')
        response = self.client.get(f'/admin-transactions/?user_id={self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('transactions', response.data)
        self.assertIn('total_balance', response.data)

    def test_admin_can_filter_transactions_by_date(self):
        self.logout_user()
        self.authenticate_user('admin', 'password')
        response = self.client.get('/admin-transactions/', {'user_id': self.user.id, 'start_date': '2024-01-01', 'end_date': '2024-01-31'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('transactions', response.data)
        self.assertEqual(len(response.data['transactions']), 1)  
        self.assertEqual(response.data['total_balance'], 300)  

class InvestmentAccountTestCase(BaseTestCase):
    
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
        self.assertEqual(self.transaction.amount, 100.00)
