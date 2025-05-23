from rest_framework import serializers
from .models import ChallengeTemplate, UserChallenge, ChallengeProgress

# ✅ 챌린지 템플릿 (이건 그대로 유지)
class ChallengeTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeTemplate
        fields = '__all__'


# ✅ 주차 or 월차 체크 정보
class ChallengeProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeProgress
        fields = ['unit_index', 'is_saved']


# ✅ 사용자 챌린지 생성/수정용
class UserChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChallenge
        fields = [
            'id', 'template', 'goal_amount', 'total_units', 'unit',
            'is_active', 'started_at', 'completed_at' 
        ]
        read_only_fields = ['id', 'is_active', 'started_at', 'completed_at' ]


# ✅ 사용자 챌린지 상세 조회용 (체크 정보 포함)
class UserChallengeDetailSerializer(serializers.ModelSerializer):
    progresses = ChallengeProgressSerializer(many=True, read_only=True)
    template_name = serializers.CharField(source='template.name', read_only=True)

    class Meta:
        model = UserChallenge
        fields = [
            'id', 'template', 'template_name',
            'goal_amount', 'total_units', 'unit',
            'is_active', 'started_at',
            'progresses', 'completed_at',
        ]
        read_only_fields = ['id', 'template_name', 'is_active', 'started_at', 'completed_at']
