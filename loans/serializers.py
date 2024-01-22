# serializers.py
from rest_framework import serializers
from .models import Bank, LoanProvider, Loan, LoanCustomer, LoanApplication

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class LoanProviderSerializer(serializers.ModelSerializer):
    bank_name = serializers.SerializerMethodField()
    class Meta:
        model = LoanProvider
        fields = ['id','LoanProviderName','budget','bank_name', 'bank'] # I dont want to show the id of the bank, rather the name to make it more readable
    
    def get_bank_name(self, obj):
        return obj.bank.name
        
        
class LoanSerializer(serializers.ModelSerializer):
    bank_name = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['id', 'bank_name', 'term', 'interest_rate', 'max_amount', 'min_amount']

    def get_bank_name(self, obj):
        return obj.bank.name

class LoanCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanCustomer
        fields = '__all__'

class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields='__all__'
       # exclude = ['amount_to_pay'] # since it's calculated internally, i dont want it to be shown to the user  
       
       
    amount_to_pay = serializers.ReadOnlyField()
    fully_paid=serializers.ReadOnlyField()