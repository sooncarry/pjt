from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import FinanceTerm, NewsItem
from .serializers import FinanceTermSerializer, NewsItemSerializer

@api_view(['GET'])
def finance_terms(request):
    """
    GET /api/terms/?q=<검색어>
    - title, eng_title, content 필드에서 부분 검색
    """
    q = request.GET.get('q', '')
    if q:
        terms = FinanceTerm.objects.filter(
            Q(title__icontains=q) |
            Q(eng_title__icontains=q) |
            Q(content__icontains=q)
        )
    else:
        terms = FinanceTerm.objects.all()

    serializer = FinanceTermSerializer(terms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def news_list(request):
    """
    GET /api/news/?search=<검색어>&page=<페이지번호>
    - category='금융' 고정 필터
    - title, summary 필드에서 부분 검색
    - published_at 내림차순 정렬
    - 페이지당 9개, 페이지네이션 정보 반환
    """
    search_query = request.GET.get('search', '')
    page = int(request.GET.get('page', 1))

    # 기본 금융 카테고리 필터
    queryset = NewsItem.objects.filter(category='금융')

    # 검색어 필터
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(summary__icontains=search_query)
        )

    # 최신순 정렬
    queryset = queryset.order_by('-published_at')

    # Django Paginator 사용
    paginator = Paginator(queryset, 9)
    page_obj = paginator.get_page(page)

    serializer = NewsItemSerializer(page_obj.object_list, many=True)
    return Response({
        'results': serializer.data,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'total_items': paginator.count,
    })
