# serializers.py
from rest_framework import serializers
from .models import Bank, LoanProvider, Loan, LoanCustomer, LoanApplication

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class LoanProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProvider
        fields = '__all__'
        
        
        
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
        fields = '__all__'
