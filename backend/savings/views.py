# savings/views.py
from django.utils.timezone import now
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    ChallengeTemplate,
    UserChallenge,
    ChallengeProgress,
)
from .serializers import (
    ChallengeTemplateSerializer,
    UserChallengeSerializer,
    UserChallengeDetailSerializer,
)

# ────────────────────────────────────────────────
# 1) 챌린지 템플릿 (읽기 전용)
class ChallengeTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChallengeTemplate.objects.all()
    serializer_class = ChallengeTemplateSerializer


# ────────────────────────────────────────────────
# 2) 진행 중인 챌린지 1개(단일) 가져오기
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_challenge(request):
    try:
        uc = UserChallenge.objects.get(user=request.user, is_active=True)
        return Response(UserChallengeDetailSerializer(uc).data)
    except UserChallenge.DoesNotExist:
        return Response(
            {"detail": "진행 중인 챌린지가 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )


# ────────────────────────────────────────────────
# 3) 새 챌린지 시작
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_challenge(request):
    template_id = request.data.get("template")
    goal_amount = request.data.get("goal_amount")
    total_units = request.data.get("total_units")
    unit        = request.data.get("unit")

    if not all([template_id, goal_amount, total_units, unit]):
        return Response(
            {"detail": "모든 필드가 필요합니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if UserChallenge.objects.filter(
        user=request.user,
        template_id=template_id,
        is_active=True,
    ).exists():
        return Response(
            {"detail": "이미 진행 중인 챌린지입니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    uc = UserChallenge.objects.create(
        user=request.user,
        template_id=template_id,
        goal_amount=goal_amount,
        total_units=total_units,
        unit=unit,
        is_active=True,
    )

    # 진행 체크 리스트 미리 생성
    ChallengeProgress.objects.bulk_create(
        [
            ChallengeProgress(user_challenge=uc, unit_index=i)
            for i in range(int(total_units))
        ]
    )

    return Response(
        UserChallengeDetailSerializer(uc).data,
        status=status.HTTP_201_CREATED,
    )


# ────────────────────────────────────────────────
# 4) 현재 챌린지 일부 수정
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_current_challenge(request):
    uc_id = request.data.get("id")
    if not uc_id:
        return Response(
            {"detail": "챌린지 ID가 필요합니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        uc = UserChallenge.objects.get(id=uc_id, user=request.user)
    except UserChallenge.DoesNotExist:
        return Response(
            {"detail": "챌린지를 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )

    ser = UserChallengeSerializer(uc, data=request.data, partial=True)
    if ser.is_valid():
        ser.save()
        return Response(UserChallengeDetailSerializer(uc).data)

    return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


# ────────────────────────────────────────────────
# 5) 특정 일/주/월 체크 토글
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_check(request):
    uc_id      = request.data.get("challenge_id")
    unit_index = request.data.get("unit_index")

    if uc_id is None or unit_index is None:
        return Response(
            {"detail": "challenge_id와 unit_index가 필요합니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        uc = UserChallenge.objects.get(
            id=uc_id, user=request.user, is_active=True
        )
        prog = ChallengeProgress.objects.get(
            user_challenge=uc, unit_index=unit_index
        )
    except (UserChallenge.DoesNotExist, ChallengeProgress.DoesNotExist):
        return Response(
            {"detail": "해당 챌린지 또는 체크 항목을 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )

    prog.is_saved = not prog.is_saved
    prog.save()

    return Response(
        {
            "challenge_id": uc_id,
            "unit_index": unit_index,
            "is_saved": prog.is_saved,
        }
    )


# ────────────────────────────────────────────────
# 6) 챌린지 종료
#    success=True  → 목표 달성  (completed_at 기록)
#    success=False → 중도 포기 (completed_at 비워둠)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def end_challenge(request):
    uc_id   = request.data.get("id")
    success = bool(request.data.get("success", False))

    if not uc_id:
        return Response(
            {"detail": "챌린지 ID가 필요합니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        uc = UserChallenge.objects.get(
            id=uc_id, user=request.user, is_active=True
        )
    except UserChallenge.DoesNotExist:
        return Response(
            {"detail": "해당 챌린지를 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )

    uc.is_active = False
    uc.completed_at = now().date() if success else None
    uc.save()

    return Response(
        {
            "detail": f"챌린지 {uc.id}를 "
                      f'{"완료" if success else "포기"}했습니다.'
        }
    )


# ────────────────────────────────────────────────
# 7) 리스트 엔드포인트
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def active_challenges(request):
    qs = UserChallenge.objects.filter(user=request.user, is_active=True)
    return Response(UserChallengeDetailSerializer(qs, many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def completed_challenges(request):
    # completed_at 값이 있는 챌린지만 성공으로 간주
    qs = UserChallenge.objects.filter(
        user=request.user,
        is_active=False,
        completed_at__isnull=False,
    ).order_by("-completed_at")
    return Response(UserChallengeDetailSerializer(qs, many=True).data)
