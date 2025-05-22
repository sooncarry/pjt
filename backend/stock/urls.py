from django.urls import path
from .views import (
    compare_stocks,
    search_corp,
    search_stock_autocomplete,
    disclosures_view,
)

urlpatterns = [
    path('compare/', compare_stocks, name='compare-stocks'),             # 📊 주식 비교
    path('search/', search_corp, name='search-corp'),                    # 📄 공시용 기업명 검색
    path('autocomplete/', search_stock_autocomplete, name='autocomplete'),  # 🔍 자동완성용
    path('disclosures/', disclosures_view, name='disclosures'),         # 📑 공시 목록
]
