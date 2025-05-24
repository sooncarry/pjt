from django.urls import path
from .views import finance_terms, news_list

urlpatterns = [
    path('finance-terms/', finance_terms, name='finance-terms'),
    path('', news_list, name='news-list'),
]
