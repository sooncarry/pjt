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
    options = serializers.SerializerMethodField()

    class Meta:
        model = QuizQuestion
        fields = ['id', 'question', 'options', 'answer', 'explanation']

    def get_options(self, obj):
        return obj.options()