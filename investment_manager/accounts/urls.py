from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import InvestmentAccountViewSet, TransactionViewSet,AdminTransactionViewSet

router = DefaultRouter()
router.register(r'accounts', InvestmentAccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('admin-transactions/', AdminTransactionViewSet.as_view({'get': 'list_user_transactions'})),

]
