from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FinanceTerm, NewsItem
from .serializers import FinanceTermSerializer, NewsItemSerializer
from django.core.paginator import Paginator

@api_view(['GET'])
def finance_terms(request):
    query = request.GET.get('q', '')
    if query:
        terms = FinanceTerm.objects.filter(
            title__icontains=query
        ) | FinanceTerm.objects.filter(
            eng_title__icontains=query
        ) | FinanceTerm.objects.filter(
            content__icontains=query
        )
    else:
        terms = FinanceTerm.objects.all()
    serializer = FinanceTermSerializer(terms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def news_list(request):
    search_query = request.GET.get('search', '')
    page = int(request.GET.get('page', 1))

    # 검색어가 있을 경우 제목과 요약에서 필터
    queryset = NewsItem.objects.all()
    if search_query:
        queryset = queryset.filter(
            title__icontains=search_query
        ) | queryset.filter(
            summary__icontains=search_query
        )

    queryset = queryset.order_by('-published_at')
    paginator = Paginator(queryset, 9)  # 페이지당 9개씩
    page_obj = paginator.get_page(page)
    serializer = NewsItemSerializer(page_obj.object_list, many=True)

    return Response({
        'results': serializer.data,
        'total_pages': paginator.num_pages,
        'current_page': page,
        'total_items': paginator.count,
    })