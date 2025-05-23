from django.urls import path
from .views import compare_stocks, search_stock_autocomplete, disclosures_view

urlpatterns = [
    path('disclosures/', disclosures_view),
    path('autocomplete/', search_stock_autocomplete),
    path('compare/', compare_stocks),
    
]
