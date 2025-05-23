from rest_framework import serializers
from .models import FinanceTerm

class FinanceTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceTerm
        fields = '__all__'
