from django.urls import path
from . import views

urlpatterns = [
    path('disclosures/', views.disclosures_view),
    path('search/', views.search_corporations),  # 자동완성용 검색 API
]
