# backend/finance/views.py

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework.permissions import AllowAny

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