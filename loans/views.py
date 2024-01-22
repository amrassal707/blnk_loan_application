# views.py
from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Bank, LoanProvider, Loan, LoanCustomer, LoanApplication
from .serializers import BankSerializer, LoanProviderSerializer, LoanSerializer, LoanCustomerSerializer, LoanApplicationSerializer


class BankListCreateView(generics.ListCreateAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method: 
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

class LoanProviderView(generics.ListCreateAPIView):
    queryset = LoanProvider.objects.all()
    serializer_class = LoanProviderSerializer
    
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method: 
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        name = self.kwargs.get('name', None)
        if name is not None:
            return LoanProvider.objects.filter(LoanProviderName=name)
        else:
            return LoanProvider.objects.all()
        
        
    def perform_create(self, serializer):
        # Get the bank associated with the new loan provider
        bank = serializer.validated_data['bank']

        # Update the bank's balance
        bank.total_funds += serializer.validated_data['budget']
        bank.save()

        # Save the new loan provider
        serializer.save()

    def perform_update(self, serializer):
        # Get the bank associated with the loan provider
        bank = serializer.instance.bank

        # Calculate the difference in budget before and after the update
        budget_difference = serializer.validated_data['budget'] - serializer.instance.budget

        # Update the bank's balance
        bank.total_funds += budget_difference
        bank.save()

        # Save the updated loan provider
        serializer.save 
    

class LoanListCreateView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method: 
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Get the bank associated with the new loan
        bank = serializer.validated_data['bank']

        # Get the loan amount from the serializer
        loan_amount = serializer.validated_data['max_amount']

        # Calculate the 25% of the bank's total funds
        twenty_five_percent_of_funds = 0.25 * float(bank.total_funds)

        # Check if the bank has sufficient funds
        if twenty_five_percent_of_funds < float(loan_amount):
            # raise error to stop serializer.save() from getting executed, because if you return a response, the serializer will still be executed
             raise serializers.ValidationError('Bank does not have sufficient funds (25% capital requirement not met).')

        # Deduct the loan amount from the bank's balance
        bank.total_funds -= loan_amount  # Convert to Decimal if not already
        bank.save()
        # Save the new loan
        serializer.save()
    
    
    

class LoanCustomerDetailView(generics.ListCreateAPIView):
    queryset = LoanCustomer.objects.all()
    serializer_class = LoanCustomerSerializer
    def get_permissions(self):
        permission_classes = []
        if self.request.method: 
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class LoanApplicationCreateView(generics.ListCreateAPIView):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer

    def perform_create(self, serializer):
        loan = serializer.validated_data['loan']
        amount = serializer.validated_data['amount']
        user = serializer.validated_data['LoanCustomer']
        bank = loan.bank

        # Check if the user already has a loan
        if user.loan:
            raise serializers.ValidationError({"error": "User already has a loan"})

        # Check if the loan amount is within the bank's available funds
        if amount > bank.total_funds:
            raise serializers.ValidationError({"error": "Loan amount exceeds available funds of the bank"})

        if not (loan.min_amount <= float(amount) <= loan.max_amount):
            raise serializers.ValidationError({"error": "Loan amount is outside the allowed range"})

        # Proceed with creating the loan application
        super().perform_create(serializer)  # Call the parent class's perform_create method

        # Deduct the loan amount from the bank's available funds
        bank.total_funds -= amount
        bank.save()

        # Associate the loan with the user
        user.loan = True
        #user.balance -= amount
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)