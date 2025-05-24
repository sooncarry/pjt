from rest_framework import serializers
from .models import FinanceTerm, NewsItem

class FinanceTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceTerm
        fields = '__all__'

class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = '__all__'
