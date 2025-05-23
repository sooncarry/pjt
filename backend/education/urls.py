from django.urls import path
from .views import finance_terms

urlpatterns = [
    path('finance-terms/', finance_terms),
]
