# stock/serializers.py
from rest_framework import serializers
from .models import StockKnowledge

class StockKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockKnowledge
        fields = '__all__'
