from django.contrib import admin
from .models import InvestmentAccount, AccountPermission, Transaction

admin.site.register(InvestmentAccount)
admin.site.register(AccountPermission)
admin.site.register(Transaction)
