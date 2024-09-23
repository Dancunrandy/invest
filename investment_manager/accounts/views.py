from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils.dateparse import parse_datetime
from django.db import models
from .models import InvestmentAccount, Transaction, AccountPermission
from .serializers import InvestmentAccountSerializer, TransactionSerializer
from .permissions import HasAccountPermission

class InvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    permission_classes = [IsAuthenticated, HasAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(users=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, HasAccountPermission]

    def perform_create(self, serializer):
        account = serializer.validated_data.get('account') 
        
        try:
            account_permission = AccountPermission.objects.get(user=self.request.user, account=account)
        except AccountPermission.DoesNotExist:
            raise PermissionDenied("You do not have permission to create transactions.")

        if account_permission.permission in ['crud', 'post']:
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied("You do not have permission to create transactions.")

    def get_queryset(self):
        return self.queryset.filter(account__users=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class AdminTransactionViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['get'], url_path='admin-transactions')
    def list_user_transactions(self, request):
        user_id = request.query_params.get('user_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        transactions = Transaction.objects.filter(user__id=user_id)

        if start_date:
            start_date = parse_datetime(start_date)
            if start_date is None:
                return Response({'error': 'Invalid start date format.'}, status=status.HTTP_400_BAD_REQUEST)
            transactions = transactions.filter(timestamp__gte=start_date)

        if end_date:
            end_date = parse_datetime(end_date)
            if end_date is None:
                return Response({'error': 'Invalid end date format.'}, status=status.HTTP_400_BAD_REQUEST)
            transactions = transactions.filter(timestamp__lte=end_date)

        total_balance = transactions.aggregate(total=models.Sum('amount'))['total'] or 0

        data = {
            'transactions': TransactionSerializer(transactions, many=True).data,
            'total_balance': total_balance,
        }

        return Response(data)
