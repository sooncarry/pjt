from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_GET
import requests
from datetime import datetime
import pandas as pd
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import yfinance as yf
from .utils.stock_compare import get_stock_comparison_data
from rest_framework import generics
from .models import StockKnowledge
from .serializers import StockKnowledgeSerializer

# CSV 로드 함수
def load_corp_codes():
    path = os.path.join(os.path.dirname(__file__), 'utils', 'corp_codes.csv')
    if not os.path.exists(path):
        return pd.DataFrame(columns=['corp_name', 'corp_code', 'stock_code'])
    return pd.read_csv(path, dtype=str)

CORP_CODE_DF = load_corp_codes()
CORP_CODE_MAP = dict(zip(CORP_CODE_DF['corp_name'], CORP_CODE_DF['corp_code']))

# 기업명으로 corp_code 조회
def get_corp_code(name):
    return CORP_CODE_MAP.get(name)

# 🔍 자동완성용 검색 API
@require_GET
def search_stock_autocomplete(request):
    query = request.GET.get('query', '').strip()
    if not query or CORP_CODE_DF.empty:
        return JsonResponse([], safe=False)

    matched = CORP_CODE_DF[
        CORP_CODE_DF['corp_name'].str.contains(query) &
        CORP_CODE_DF['stock_code'].notna() &
        (CORP_CODE_DF['stock_code'] != '') &
        (CORP_CODE_DF['stock_code'] != '0')
    ]

    result = [
        {
            'name': row['corp_name'],
            'code': str(row['stock_code']).zfill(6)
        }
        for _, row in matched.head(20).iterrows()
    ]
    return JsonResponse(result, safe=False)

# 📄 공시정보 API
@require_GET
def disclosures_view(request):
    query = request.GET.get('query', '').strip()
    corp_code = get_corp_code(query) if query else None
    if query and not corp_code:
        return JsonResponse({'disclosures': []})

    bgn_de = request.GET.get('bgn_de', '')
    end_de = request.GET.get('end_de', datetime.today().strftime('%Y%m%d'))

    page_group = int(request.GET.get('page_group', '1'))
    page_count = 100 * page_group
    page_no = int(request.GET.get('page_no', '1'))
    params = {
        'crtfc_key': settings.DART_API_KEY,
        'bgn_de': bgn_de,
        'end_de': end_de,
        'page_count': 100,
        'page_no': page_no,
    }
    if corp_code:
        params['corp_code'] = corp_code

    url = 'https://opendart.fss.or.kr/api/list.json'
    res = requests.get(url, params=params)
    try:
        data = res.json()
    except Exception:
        return JsonResponse({'error': 'Invalid response'}, status=500)

    if data.get('status') != '000':
        return JsonResponse({'disclosures': []})

    result = []
    for item in data.get('list', []):
        result.append({
            'title': item.get('report_nm'),
            'date': item.get('rcept_dt'),
            'corp_name': item.get('corp_name'),
            'link': f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={item.get('rcept_no')}"
        })

    return JsonResponse({'disclosures': result})

@api_view(['POST'])
@permission_classes([AllowAny])
def compare_stocks(request):
    codes = request.data.get('codes', [])
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')

    if not codes or not start_date or not end_date:
        return Response({'error': 'codes, start_date, end_date are required.'},
                        status=status.HTTP_400_BAD_REQUEST)

    result = []
    for code in codes:
        data = get_stock_comparison_data(code, start_date, end_date)
        if data:
            result.append(data)
        else:
            result.append({
                'code': code,
                'name': '조회 실패',
                'price_change_rate': 0,
                'avg_volume': 0,
                'dividend': {
                    'amount': 0,
                    'yield': 0.0,
                    'date': '-'
                },
                'per': None,
                'pbr': None,
                'market_cap': None,
                'sector': '-',
                'industry': '-',
                'history': []
            })

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_stock_name(request):
    code = request.GET.get('code', '').strip()
    if not code or CORP_CODE_DF.empty:
        return Response({'error': '코드가 제공되지 않았습니다.'}, status=400)

    matched = CORP_CODE_DF[
        CORP_CODE_DF['stock_code'].notna() &
        (CORP_CODE_DF['stock_code'] != '') &
        (CORP_CODE_DF['stock_code'] != '0') &
        (CORP_CODE_DF['stock_code'] == code.zfill(6))
    ]

    if matched.empty:
        return Response({'error': '일치하는 기업이 없습니다.'}, status=404)

    corp_name = matched.iloc[0]['corp_name']
    return Response({'name': corp_name})

class StockKnowledgeListView(generics.ListAPIView):
    queryset = StockKnowledge.objects.all()
    serializer_class = StockKnowledgeSerializer

class StockKnowledgeDetailView(generics.RetrieveAPIView):
    queryset = StockKnowledge.objects.all()
    serializer_class = StockKnowledgeSerializer