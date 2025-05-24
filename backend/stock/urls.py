from django.urls import path
from .views import compare_stocks, search_stock_autocomplete, disclosures_view
from .views import StockKnowledgeListView, StockKnowledgeDetailView

urlpatterns = [
    path('disclosures/', disclosures_view),
    path('autocomplete/', search_stock_autocomplete),
    path('compare/', compare_stocks),
    path('knowledge/', StockKnowledgeListView.as_view(), name='knowledge-list'),
    path('knowledge/<int:pk>/', StockKnowledgeDetailView.as_view(), name='knowledge-detail'),
    
]
