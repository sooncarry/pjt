# backend/finance/urls.py
from django.urls import path
from .views import DepositProductData, SavingProductData, RecommendProducts, check_financial_profile

urlpatterns = [
    path('deposit-products/', DepositProductData.as_view(), name='deposit_products'),
    path('saving-products/', SavingProductData.as_view(), name='saving_products'),
    # path('recommend-products/', recommend_products),
    path('recommend-products/', RecommendProducts.as_view()),
    path('check-profile/', check_financial_profile), 
]