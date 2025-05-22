from rest_framework import serializers
from .models import ChallengeTemplate, SavingChallenge, SavingCheck

class ChallengeTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeTemplate
        fields = '__all__'

class SavingCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingCheck
        fields = ['date', 'is_saved']

class SavingChallengeSerializer(serializers.ModelSerializer):
    checks = SavingCheckSerializer(many=True, read_only=True)

    class Meta:
        model = SavingChallenge
        fields = '__all__'
        read_only_fields = ['user', 'weekly_saving', 'total_weeks']
        
