from rest_framework import serializers
from .models import FinanceTerm, NewsItem

class FinanceTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceTerm
        fields = '__all__'


class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = [
            'id',
            'title',
            'summary',
            'url',
            'published_at',
            'source',
            'thumbnail',
            'category',
        ]