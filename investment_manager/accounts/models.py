from django.contrib.auth.models import User
from django.db import models

class InvestmentAccount(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, through='AccountPermission')

    def __str__(self):
        return self.name

class AccountPermission(models.Model):
    PERMISSION_CHOICES = [
        ('view', 'View Only'),
        ('crud', 'Full Access (CRUD)'),
        ('post', 'Post Transactions Only'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    def __str__(self):
        return f'{self.user.username} - {self.account.name} ({self.permission})'

class Transaction(models.Model):
    account = models.ForeignKey(InvestmentAccount, related_name='transactions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.amount} - {self.account.name} by {self.user.username}'
