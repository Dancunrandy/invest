from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from .models import InvestmentAccount, Transaction, AccountPermission

class BaseTestCase(APITestCase):
    def setUp(self):
        # Create a default user and account for base tests
        self.user = User.objects.create_user(username='testuser', password='password')
        self.account = InvestmentAccount.objects.create(name='Test Account')
        AccountPermission.objects.create(user=self.user, account=self.account, permission='crud')
        self.transaction = Transaction.objects.create(account=self.account, user=self.user, amount=100.00, timestamp=timezone.now())
    
    def authenticate_user(self, username, password):
        self.client.login(username=username, password=password)
    
    def logout_user(self):
        self.client.logout()

class UserPermissionsTests(BaseTestCase):
    
    def setUp(self):
        super().setUp()  # Call the base setup
        
        # Create user and admin
        self.user = User.objects.create_user(username='user', password='password')
        self.admin = User.objects.create_superuser(username='admin', password='password')

        # Authenticate the user for the tests
        self.authenticate_user('user', 'password')

        # Create investment accounts for different permission levels
        self.account1 = InvestmentAccount.objects.create(name='View Only Account')
        self.account2 = InvestmentAccount.objects.create(name='CRUD Account')
        self.account3 = InvestmentAccount.objects.create(name='Post Only Account')

        # Assign permissions to the user
        AccountPermission.objects.create(user=self.user, account=self.account1, permission='view')
        AccountPermission.objects.create(user=self.user, account=self.account2, permission='crud')
        AccountPermission.objects.create(user=self.user, account=self.account3, permission='post')

        # Create transactions within specific date ranges
        self.transaction1 = Transaction.objects.create(user=self.user, account=self.account2, amount=100, timestamp=timezone.make_aware(timezone.datetime(2024, 1, 15)))
        self.transaction2 = Transaction.objects.create(user=self.user, account=self.account3, amount=200, timestamp=timezone.make_aware(timezone.datetime(2024, 1, 10)))
        self.transaction3 = Transaction.objects.create(user=self.user, account=self.account2, amount=300, timestamp=timezone.make_aware(timezone.datetime(2024, 1, 1)))
        self.transaction4 = Transaction.objects.create(user=self.user, account=self.account2, amount=400, timestamp=timezone.make_aware(timezone.datetime(2024, 2, 1)))

    def test_user_with_view_permission_cannot_create_transaction(self):
        self.authenticate_user('user', 'password')
        response = self.client.post('/api/transactions/', {'account': self.account1.id, 'amount': 500})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_with_crud_permission_can_create_transaction(self):
        self.authenticate_user('user', 'password')
        response = self.client.post('/api/transactions/', {'account': self.account2.id, 'amount': 500})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_with_post_only_permission_cannot_view_transactions(self):
        self.authenticate_user('user', 'password')
        response = self.client.get(f'/api/transactions/{self.transaction2.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_access_all_transactions(self):
        self.logout_user()
        self.authenticate_user('admin', 'password')
        response = self.client.get(f'/api/admin-transactions/?user_id={self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('transactions', response.data)
        self.assertIn('total_balance', response.data)

    def test_admin_can_filter_transactions_by_date(self):
        self.logout_user()
        self.authenticate_user('admin', 'password')
        response = self.client.get('/api/admin-transactions/', {
            'user_id': self.user.id, 
            'start_date': '2024-01-01T00:00:00Z', 
            'end_date': '2024-01-31T23:59:59Z'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('transactions', response.data)
        self.assertEqual(len(response.data['transactions']), 2)  
        self.assertEqual(response.data['total_balance'], 700)  

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
