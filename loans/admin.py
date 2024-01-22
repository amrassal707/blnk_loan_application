from django.contrib import admin
from .models import Bank, LoanProvider, Loan, LoanCustomer, LoanApplication

admin.site.register(Bank)
admin.site.register(LoanProvider)
admin.site.register(Loan)
admin.site.register(LoanCustomer)
admin.site.register(LoanApplication)
