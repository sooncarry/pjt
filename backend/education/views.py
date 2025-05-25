from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import FinanceTerm, NewsItem, QuizQuestion
from .serializers import FinanceTermSerializer, NewsItemSerializer, QuizQuestionSerializer

import random

# ✅ 금융 용어 검색 API
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

# ✅ 금융 뉴스 목록 API (페이지네이션 포함)
@api_view(['GET'])
@permission_classes([AllowAny])
def breaking_news(request):
    page = int(request.GET.get('page', 1))
    page_size = 20
    qs = NewsItem.objects.order_by('-crawled_at', '-id')  # 최신순
    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page)

    data = {
        'results': NewsItemSerializer(page_obj.object_list, many=True).data,
        'current_page': page,
        'total_pages': paginator.num_pages,
        'total_count': paginator.count,
    }
    return Response(data)

# ✅ 금융 퀴즈 API (랜덤 5개 반환)
@api_view(['GET'])
@permission_classes([AllowAny])
def quiz_question_list(request):
    quizzes = list(QuizQuestion.objects.all())
    selected = random.sample(quizzes, min(5, len(quizzes)))
    serializer = QuizQuestionSerializer(selected, many=True)
    return Response(serializer.data)
