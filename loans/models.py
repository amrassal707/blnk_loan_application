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
    amount_paid=models.DecimalField(max_digits=15, decimal_places=2, default=0)
    fully_paid=models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        # Calculate amount_to_pay based on amount and loan's interest_rate
        if self.loan:
            interest_rate_percentage = self.loan.interest_rate
            interest_rate_decimal = interest_rate_percentage / 100  # Convert percentage to decimal
            self.amount_to_pay = self.amount * (1 + interest_rate_decimal)
        super().save(*args, **kwargs)
        
    def make_payment(self, amount_paid):
        # Check if the amount_paid is a valid decimal number
        try:
            amount_paid_decimal = models.DecimalField().to_python(amount_paid)
        except (ValueError, TypeError, models.ValidationError):
            raise models.ValidationError({"error": "Amount paid must be a valid decimal number"})

        if amount_paid_decimal < 0:
            raise models.ValidationError({"error": "Amount paid must be a non-negative value"})

        # Check if the amount_paid is within the remaining amount_to_pay
        remaining_amount_to_pay = self.amount_to_pay - amount_paid_decimal
        if remaining_amount_to_pay < 0:
            raise models.ValidationError({"error": "Amount paid exceeds the remaining amount_to_pay"})

        # Update the remaining amount_to_pay
        self.amount_paid+=amount_paid_decimal
        self.save()

        # Deduct the payment from the associated user's balance
        loan_customer = self.LoanCustomer
        loan_customer.balance -= amount_paid_decimal
        loan_customer.save()
        
        # Add the payment to the bank's total funds
        bank = self.loan.bank
        bank.total_funds += amount_paid_decimal
        bank.save()