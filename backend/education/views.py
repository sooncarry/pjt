# backend/education/views.py

from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.dateparse import parse_datetime

from .models import FinanceTerm, NewsItem, QuizQuestion
from .serializers import FinanceTermSerializer, NewsItemSerializer, QuizQuestionSerializer

import random

# 금융 용어 검색 API (unchanged)
@api_view(['GET'])
def finance_terms(request):
    q = request.GET.get('q', '').strip()
    qs = FinanceTerm.objects.all()
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(eng_title__icontains=q) |
            Q(content__icontains=q)
        )
    return Response(FinanceTermSerializer(qs, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def breaking_news(request):
    page_size = int(request.GET.get('page_size', 20))
    before = request.GET.get('before', None)
    last_id = request.GET.get('last_id', None)

    qs = NewsItem.objects.order_by('-published_at', '-id')

    if before:
        before_dt = parse_datetime(before)
        if last_id:
            qs = qs.filter(
                Q(published_at__lt=before_dt) |
                Q(published_at=before_dt, id__lt=int(last_id))
            )
        else:
            qs = qs.filter(published_at__lt=before_dt)

    # page_size+1 건을 미리 읽어서 has_more 판단
    items = list(qs[:page_size + 1])
    has_more = len(items) > page_size
    items = items[:page_size]

    # 다음 커서에 사용할 published_at, id
    if has_more and items:
        last = items[-1]
        next_cursor = {
            'before': last.published_at.isoformat(),
            'last_id': last.id
        }
    else:
        next_cursor = None

    return Response({
        'results': NewsItemSerializer(items, many=True).data,
        'cursor': next_cursor,
        'has_more': has_more,
    })


# 금융 퀴즈 API (unchanged)
@api_view(['GET'])
@permission_classes([AllowAny])
def quiz_question_list(request):
    quizzes = list(QuizQuestion.objects.all())
    selected = random.sample(quizzes, min(5, len(quizzes)))
    serializer = QuizQuestionSerializer(selected, many=True)
    return Response(serializer.data)
