from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChallengeTemplate, UserChallenge, ChallengeProgress
from .serializers import (
    ChallengeTemplateSerializer,
    UserChallengeSerializer,
    UserChallengeDetailSerializer,
    ChallengeProgressSerializer,
)
from django.utils.timezone import now

# ✅ 챌린지 템플릿 리스트용 (그대로 유지)
from rest_framework import viewsets

class ChallengeTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChallengeTemplate.objects.all()
    serializer_class = ChallengeTemplateSerializer

# ✅ 현재 챌린지 불러오기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_challenge(request):
    try:
        challenge = UserChallenge.objects.get(user=request.user, is_active=True)
        serializer = UserChallengeDetailSerializer(challenge)
        return Response(serializer.data)
    except UserChallenge.DoesNotExist:
        return Response({'detail': '진행 중인 챌린지가 없습니다.'}, status=404)

# ✅ 새 챌린지 시작
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_challenge(request):
    template_id = request.data.get('template')
    goal_amount = request.data.get('goal_amount')
    total_units = request.data.get('total_units')
    unit = request.data.get('unit')

    if not all([template_id, goal_amount, total_units, unit]):
        return Response({'detail': '모든 필드가 필요합니다.'}, status=400)

    if UserChallenge.objects.filter(user=request.user, template_id=template_id, is_active=True).exists():
        return Response({'detail': '이미 진행 중인 챌린지입니다.'}, status=400)
    
    # 새 챌린지 생성
    challenge = UserChallenge.objects.create(
        user=request.user,
        template_id=template_id,
        goal_amount=goal_amount,
        total_units=total_units,
        unit=unit,
        is_active=True,
    )

    # 진행 체크 리스트 생성
    ChallengeProgress.objects.bulk_create([
        ChallengeProgress(user_challenge=challenge, unit_index=i)
        for i in range(int(total_units))
    ])

    return Response(UserChallengeDetailSerializer(challenge).data, status=201)

# ✅ 챌린지 수정
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_current_challenge(request):
    challenge_id = request.data.get('id')

    if not challenge_id:
        return Response({'detail': '챌린지 ID가 필요합니다.'}, status=400)

    try:
        challenge = UserChallenge.objects.get(id=challenge_id, user=request.user)
    except UserChallenge.DoesNotExist:
        return Response({'detail': '챌린지를 찾을 수 없습니다.'}, status=404)

    serializer = UserChallengeSerializer(challenge, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(UserChallengeDetailSerializer(challenge).data)
    return Response(serializer.errors, status=400)



# ✅ 특정 주차 or 월차 체크 토글
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_check(request):
    challenge_id = request.data.get('challenge_id')
    unit_index = request.data.get('unit_index')

    if challenge_id is None or unit_index is None:
        return Response({'detail': 'challenge_id와 unit_index가 필요합니다.'}, status=400)

    try:
        challenge = UserChallenge.objects.get(id=challenge_id, user=request.user, is_active=True)
        progress = ChallengeProgress.objects.get(user_challenge=challenge, unit_index=unit_index)
    except (UserChallenge.DoesNotExist, ChallengeProgress.DoesNotExist):
        return Response({'detail': '해당 챌린지 또는 체크 항목을 찾을 수 없습니다.'}, status=404)

    progress.is_saved = not progress.is_saved
    progress.save()

    return Response({
        'challenge_id': challenge_id,
        'unit_index': unit_index,
        'is_saved': progress.is_saved
    })


# ✅ 챌린지 종료
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def end_challenge(request):
    challenge_id = request.data.get('id')

    if not challenge_id:
        return Response({'detail': '챌린지 ID가 필요합니다.'}, status=400)

    try:
        challenge = UserChallenge.objects.get(id=challenge_id, user=request.user, is_active=True)
        challenge.is_active = False
        challenge.completed_at = now().date() 
        challenge.save()
        return Response({'detail': f'챌린지 {challenge.id}를 종료했습니다.'})
    except UserChallenge.DoesNotExist:
        return Response({'detail': '해당 챌린지를 찾을 수 없습니다.'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def active_challenges(request):
    challenges = UserChallenge.objects.filter(user=request.user, is_active=True)
    serializer = UserChallengeDetailSerializer(challenges, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def completed_challenges(request):
    challenges = UserChallenge.objects.filter(user=request.user, is_active=False)
    serializer = UserChallengeDetailSerializer(challenges, many=True)
    return Response(serializer.data)