import requests
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime, timedelta
from stock.utils.corpcode import get_corp_code
import pandas as pd
import os

def disclosures_view(request):
    query = request.GET.get('query')
    bgn_de = request.GET.get('bgn_de')
    page_group = int(request.GET.get('page_group', 1))  # ✅ 기본값 1

    # 기본 날짜 설정: 최근 3개월
    if not bgn_de:
        start_date = datetime.today() - timedelta(days=90)
        bgn_de = start_date.strftime('%Y%m%d')
    end_de = datetime.today().strftime('%Y%m%d')

    # 전체 공시 vs 기업 공시
    params = {
        'crtfc_key': settings.DART_API_KEY,
        'bgn_de': bgn_de,
        'end_de': end_de,
        'page_count': 100,
        'page_no': page_group,  # ✅ 핵심 포인트
    }

    if query:
        corp_code = get_corp_code(query)
        if not corp_code:
            return JsonResponse({'disclosures': [], 'page_group': page_group})
        params['corp_code'] = corp_code

    url = 'https://opendart.fss.or.kr/api/list.json'
    res = requests.get(url, params=params)

    if res.status_code != 200:
        return JsonResponse({'error': '공시 요청 실패'}, status=500)

    data = res.json()
    if data.get('status') != '000':
        return JsonResponse({'disclosures': [], 'page_group': page_group})

    result = [
        {
            'title': item.get('report_nm'),
            'date': item.get('rcept_dt'),
            'corp_name': item.get('corp_name'),
            'link': f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={item.get('rcept_no')}",
        }
        for item in data.get('list', [])
    ]

    return JsonResponse({'disclosures': result, 'page_group': page_group})


CSV_PATH = os.path.join(os.path.dirname(__file__), 'utils', 'corp_codes.csv')
def search_corporations(request):
    query = request.GET.get('query', '').strip()
    if not query:
        return JsonResponse([], safe=False)

    try:
        df = pd.read_csv(CSV_PATH, dtype=str)
        # 이름에 query가 포함된 기업만 검색 (최대 10개 제한)
        matches = df[df['corp_name'].str.contains(query, na=False)].head(10)

        results = [{'name': row['corp_name']} for _, row in matches.iterrows()]
        return JsonResponse(results, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)