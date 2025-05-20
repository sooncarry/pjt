# backend/finance/urls.py
from django.urls import path
from .views import DepositProductData

urlpatterns = [
    path('api/deposit-products/', DepositProductData.as_view(), name='deposit_products'),
]
