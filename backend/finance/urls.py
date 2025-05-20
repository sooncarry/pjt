# backend/finance/urls.py
from django.urls import path
from .views import DepositProductData, SavingProductData

urlpatterns = [
    path('api/deposit-products/', DepositProductData.as_view(), name='deposit_products'),
    path('api/saving-products/', SavingProductData.as_view(), name='saving_products'),
]
