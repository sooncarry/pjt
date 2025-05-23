# backend/finance/views.py

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from .models import DepositProduct
from .serializers import DepositProductSerializer

class DepositProductData(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        api_key = settings.FINLIFE_API_KEY  # 금감원에서 발급한 실제 인증키 사용
        url = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
        params = {
            "auth": api_key,
            "topFinGrpNo": "020000",  # 020000 = 은행
            "pageNo": "1"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            result = response.json().get("result", {})

            # baseList: 기본 정보, optionList: 금리/조건 등 옵션
            return Response(result)

        except requests.exceptions.RequestException as e:
            return Response({"error": "API 요청 실패", "detail": str(e)}, status=500)
        except Exception as e:
            return Response({"error": "알 수 없는 오류", "detail": str(e)}, status=500)

class SavingProductData(APIView):
    def get(self, request):
        api_key = settings.FINLIFE_API_KEY
        url = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
        params = {
            "auth": api_key,
            "topFinGrpNo": "020000",  # 은행
            "pageNo": "1"
        }

        try:
            res = requests.get(url, params=params)
            res.raise_for_status()
            data = res.json().get("result", {}).get("baseList", [])
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

# @api_view(['GET'])
# def recommend_products(request):
#     income = int(request.GET.get('monthly_income', 0))
#     products = DepositProduct.objects.filter(min_amount__lte=income).order_by('-interest_rate')[:3]
#     serializer = DepositProductSerializer(products, many=True)
#     return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
import requests

class RecommendProducts(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        income = int(request.GET.get('monthly_income', 0))
        product_type = request.GET.get('type', 'all')  # 'deposit', 'saving', 'all'
        term = request.GET.get('term')  # 가입기간 필터링: 예) '12', '24'

        api_key = settings.FINLIFE_API_KEY
        base_url = "http://finlife.fss.or.kr/finlifeapi/"

        endpoints = {
            'deposit': "depositProductsSearch.json",
            'saving': "savingProductsSearch.json"
        }

        try:
            results = []

            for kind, endpoint in endpoints.items():
                if product_type != 'all' and product_type != kind:
                    continue

                response = requests.get(base_url + endpoint, params={
                    "auth": api_key,
                    "topFinGrpNo": "020000",
                    "pageNo": "1"
                })
                response.raise_for_status()
                data = response.json().get("result", {})
                base_list = data.get("baseList", [])
                option_list = data.get("optionList", [])

                for option in option_list:
                    rate = option.get("intr_rate")
                    if not rate:
                        continue

                    join_term = option.get("save_trm")  # 저장기간
                    if term and join_term != term:
                        continue

                    # 예: 가입금액 조건이 따로 없을 경우 모두 통과시킴
                    # (금감원 API에는 정확한 최소가입금액 정보 없음)
                    prdt_cd = option.get("fin_prdt_cd")
                    matched_base = next((b for b in base_list if b.get("fin_prdt_cd") == prdt_cd), None)
                    if not matched_base:
                        continue

                    results.append({
                        "id": prdt_cd,
                        "type": kind,
                        "name": matched_base["kor_co_nm"] + " - " + matched_base["fin_prdt_nm"],
                        "interest_rate": float(rate),
                        "term": join_term,
                        "join_deny": matched_base.get("join_deny"),
                        "etc_note": matched_base.get("etc_note"),
                    })

            # 금리 기준 상위 3개만 반환
            results = sorted(results, key=lambda x: x["interest_rate"], reverse=True)[:3]
            return Response(results)

        except requests.exceptions.RequestException as e:
            return Response({"error": "API 요청 실패", "detail": str(e)}, status=500)
        except Exception as e:
            return Response({"error": "알 수 없는 오류", "detail": str(e)}, status=500)
