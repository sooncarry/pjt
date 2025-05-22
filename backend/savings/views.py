from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ChallengeTemplate, SavingChallenge, SavingCheck
from .serializers import *

from datetime import timedelta, date

class ChallengeTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChallengeTemplate.objects.all()
    serializer_class = ChallengeTemplateSerializer

class SavingChallengeViewSet(viewsets.ModelViewSet):
    queryset = SavingChallenge.objects.all()
    serializer_class = SavingChallengeSerializer

    def perform_create(self, serializer):
        income = self.request.data.get("income")
        fixed = self.request.data.get("fixed_expenses")
        luxury = self.request.data.get("luxury_budget")
        goal = self.request.data.get("goal_amount")

        available = int(income) - int(fixed) - int(luxury)
        if available <= 0:
            raise serializers.ValidationError("저축 가능한 금액이 없습니다.")

        weeks = (int(goal) // available) + 1
        instance = serializer.save(user=self.request.user, weekly_saving=available, total_weeks=weeks)

        for i in range(weeks):
            SavingCheck.objects.create(
                challenge=instance,
                date=date.today() + timedelta(weeks=i),
                is_saved=False
            )

    @action(detail=True, methods=["post"])
    def check(self, request, pk=None):
        challenge = self.get_object()
        date_str = request.data.get("date")
        check = challenge.checks.filter(date=date_str).first()
        if check:
            check.is_saved = True
            check.save()
            return Response({"message": "성공적으로 체크되었습니다."})
        return Response({"error": "해당 날짜의 항목이 없습니다."}, status=400)
