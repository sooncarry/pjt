from django.urls import path
from .views import finance_terms, news_list

urlpatterns = [
    path('finance-terms/', finance_terms),
    path('news_list/', news_list),
]
