# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    pass


# Make your custom User model swappable
User._meta.swappable = 'AUTH_USER_MODEL'
class Bank(models.Model):
    name = models.CharField(max_length=255)
    total_funds = models.DecimalField(max_digits=15, decimal_places=2)
    def __str__(self) -> str:
        return self.name 


class LoanProvider(models.Model):
    LoanProviderName=models.CharField(max_length=255)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    def __str__(self) -> str:
        return self.LoanProviderName 
    

class Loan(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    term = models.IntegerField()  # in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    max_amount = models.DecimalField(max_digits=15, decimal_places=2)
    min_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self) -> str:
        return str(self.bank) + " rate " + str(self.interest_rate) + " term " +  str(self.term)
    

class LoanCustomer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loan_customer', default=1)
    balance=models.DecimalField(max_digits=15, decimal_places=2)
    loan = models.BooleanField(default=False)
    def __str__(self):
        return str(self.user.username)

class LoanApplication(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    LoanCustomer=models.ForeignKey(LoanCustomer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    amount_to_pay = models.DecimalField(max_digits=15, decimal_places=2)
    
    def save(self, *args, **kwargs):
        # Calculate amount_to_pay based on amount and loan's interest_rate
        if self.loan:
            interest_rate_percentage = self.loan.interest_rate
            interest_rate_decimal = interest_rate_percentage / 100  # Convert percentage to decimal
            self.amount_to_pay = self.amount * (1 + interest_rate_decimal)
        super().save(*args, **kwargs)
