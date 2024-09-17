from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from django.db import models

from .models import InvestmentAccount, Transaction
from .serializers import InvestmentAccountSerializer, TransactionSerializer
from .permissions import HasAccountPermission

class InvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    permission_classes = [IsAuthenticated, HasAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(users=self.request.user)

# TransactionViewSet to manage transactions
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, HasAccountPermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Filter transactions based on user's permissions and accounts
        return self.queryset.filter(account__users=self.request.user)

class AdminTransactionViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]  # Only admin can access this view

    @action(detail=False, methods=['get'], url_path='admin-transactions')
    def list_user_transactions(self, request):
        user_id = request.query_params.get('user_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        
        transactions = Transaction.objects.filter(user__id=user_id)

        if start_date:
            transactions = transactions.filter(timestamp__gte=parse_date(start_date))
        if end_date:
            transactions = transactions.filter(timestamp__lte=parse_date(end_date))

        total_balance = transactions.aggregate(total=models.Sum('amount'))['total'] or 0

        data = {
            'transactions': TransactionSerializer(transactions, many=True).data,
            'total_balance': total_balance,
        }

        return Response(data)
