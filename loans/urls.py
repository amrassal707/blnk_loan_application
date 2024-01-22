# urls.py
from django.urls import path
from .views import BankListCreateView,LoanProviderView , LoanListCreateView, LoanCustomerDetailView, LoanApplicationCreateView

urlpatterns = [
    path('banks/', BankListCreateView.as_view(), name='bank-list-create'),
    path('loan-providers/', LoanProviderView.as_view(), name='loan-provider-amortization'),
    path('loan-providers/<str:name>/', LoanProviderView.as_view(), name='loan-provider-loans'),
    path('loans/', LoanListCreateView.as_view(), name='loan-list-create'),
    path('loan-customers/', LoanCustomerDetailView.as_view(), name='loan-customer-detail'),
    path('loan-applications/', LoanApplicationCreateView.as_view(), name='loan-application-create'),
]
