from rest_framework import serializers
from .models import FinanceTerm, NewsItem, QuizQuestion


class FinanceTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceTerm
        fields = '__all__'

class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = '__all__'   # thumbnail 등 추가 필드 포함

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question', 'option1', 'option2', 'option3', 'option4', 'answer', 'explanation']
