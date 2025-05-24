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
        


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
import requests
from accounts.models import FinancialProfile

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_financial_profile(request):
    try:
        profile = FinancialProfile.objects.get(user=request.user)
        if profile.checklist_submitted:  # 설문 완료 여부
            return Response({"has_profile": True, "title": profile.title})
        else:
            return Response({"has_profile": False})
    except FinancialProfile.DoesNotExist:
        return Response({"has_profile": False})

class RecommendProducts(APIView):
    permission_classes = [AllowAny]  # 로그인 상태 체크는 프론트에서 처리

    def get(self, request):
        income = int(request.GET.get('monthly_income', 0))
        product_type = request.GET.get('type', 'all')
        term = request.GET.get('term')

        profile = None
        if request.user.is_authenticated:
            try:
                profile = FinancialProfile.objects.get(user=request.user)
            except FinancialProfile.DoesNotExist:
                pass

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

                    join_term = option.get("save_trm")
                    if term and join_term != term:
                        continue

                    prdt_cd = option.get("fin_prdt_cd")
                    base = next((b for b in base_list if b.get("fin_prdt_cd") == prdt_cd), None)
                    if not base:
                        continue

                    result = {
                        "id": prdt_cd,
                        "type": kind,
                        "name": base["kor_co_nm"] + " - " + base["fin_prdt_nm"],
                        "interest_rate": float(rate),
                        "term": join_term,
                        "etc_note": base.get("etc_note", ""),
                        "score": 0
                    }

                    result["score"] = calculate_score(result, profile)
                    results.append(result)

            sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)[:3]
            return Response(sorted_results)

        except requests.exceptions.RequestException as e:
            return Response({"error": "API 요청 실패", "detail": str(e)}, status=500)
        except Exception as e:
            return Response({"error": "알 수 없는 오류", "detail": str(e)}, status=500)

def calculate_score(product, profile):
    score = 0
    rate = product["interest_rate"]
    note = product.get("etc_note", "").lower()
    type = product["type"]

    # [1] 기본 금리 점수
    score += rate * 40

    # [2] 조건 편의성
    if "급여이체" in note or "우대" in note:
        score -= 20
    else:
        score += 30

    # [3] 사용자 성향 반영
    if profile:
        saving = profile.saving_style
        spending = profile.spending_style

        if saving == "보수적" and type == "deposit":
            score += 30
        elif saving == "공격적" and type == "saving":
            score += rate * 10

        if spending == "공격적" and "우대" not in note:
            score += 10

    return score