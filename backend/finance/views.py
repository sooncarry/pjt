# backend/finance/views.py

import re
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from .models import DepositProduct
from .serializers import DepositProductSerializer
from accounts.models import FinancialProfile

# 은행 라벨 ↔ 매칭 키워드 매핑
BANK_ALIAS = {
    "한국산업은행":       ["한국산업은행"],
    "NH농협은행":        ["NH농협은행", "농협은행주식회사", "농협은행"],
    "신한은행":          ["신한은행"],
    "우리은행":          ["우리은행"],
    "SC제일은행":        ["SC제일은행"],
    "하나은행":          ["하나은행"],
    "IBK기업은행":       ["IBK기업은행", "중소기업은행"],
    "KB국민은행":        ["KB국민은행", "국민은행"],
    "한국씨티은행":      ["한국씨티은행"],
    "Sh수협은행":       ["Sh수협은행", "수협은행"],
    "iM뱅크(구 대구은행)": ["iM뱅크", "아이엠뱅크", "대구은행"],
    "BNK부산은행":       ["BNK부산은행", "부산은행"],
    "광주은행":          ["광주은행"],
    "제주은행":          ["제주은행"],
    "전북은행":          ["전북은행"],
    "BNK경남은행":       ["BNK경남은행", "경남은행"],
    "케이뱅크":          ["케이뱅크", "주식회사 케이뱅크"],
    "카카오뱅크":        ["카카오뱅크", "주식회사 카카오뱅크"],
    "토스뱅크":          ["토스뱅크", "토스뱅크 주식회사"],
}


class DepositProductData(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # 1) 쿼리스트링 파싱
        banks     = request.query_params.getlist('banks')
        calcType  = request.query_params.get('calcType', '')
        term      = request.query_params.get('term', '')
        joinWay   = request.query_params.get('joinWay', '')
        sortBy    = request.query_params.get('sortBy', 'kor_co_nm')
        sortOrder = request.query_params.get('sortOrder', 'asc')

        # 2) 금감원 예금 API 호출
        url = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
        params = {
            "auth": settings.FINLIFE_API_KEY,
            "topFinGrpNo": "020000",
            "pageNo": "1"
        }
        try:
            resp = requests.get(url, params=params, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            return Response(
                {"error": "금감원 API 요청 실패", "detail": str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        data        = resp.json().get("result", {})
        base_list   = data.get("baseList", [])
        option_list = data.get("optionList", [])

        # 3) baseList 필터링 (은행)
        if banks:
            patterns = []
            for sel in banks:
                patterns += BANK_ALIAS.get(sel, [sel])
            base_list = [
                b for b in base_list
                if any(pat in b.get("kor_co_nm", "") for pat in patterns)
            ]
        # 4) 가입방식 필터
        if joinWay:
            base_list = [
                b for b in base_list
                if joinWay in b.get("join_way", "")
            ]

        # 5) optionList 필터링 (단리/복리, 만기)
        if calcType:
            option_list = [
                o for o in option_list
                if o.get("intr_rate_type_nm") == calcType
            ]
        if term:
            option_list = [
                o for o in option_list
                if o.get("save_trm") == term
            ]

        # 6) baseList ↔ optionList 매칭 & merge
        base_map = {b["fin_prdt_cd"]: b for b in base_list}
        merged = []
        for o in option_list:
            code = o.get("fin_prdt_cd")
            b = base_map.get(code)
            if b:
                merged.append({**b, **o})

        # 7) 상품코드별 최고 금리(intr_rate2)만 남기기
        best_map = {}
        for item in merged:
            code = item["fin_prdt_cd"]
            rate2 = float(item.get("intr_rate2") or item.get("intr_rate") or 0)
            existing = best_map.get(code)
            if not existing or rate2 > float(existing.get("intr_rate2") or existing.get("intr_rate") or 0):
                best_map[code] = item
        final_list = list(best_map.values())

        # 8) 정렬
        key_map = {
            "kor_co_nm": "kor_co_nm",
            "basicRate": "intr_rate",
            "maxRate":   "intr_rate2"
        }
        sort_key = key_map.get(sortBy, "kor_co_nm")
        reverse = (sortOrder == "desc")

        def sort_val(x):
            v = x.get(sort_key)
            return float(v) if sort_key in ("intr_rate", "intr_rate2") else (v or "")

        final_list.sort(key=sort_val, reverse=reverse)

        # 9) 결과 반환
        return Response({"baseList": final_list}, status=status.HTTP_200_OK)


class SavingProductData(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # 1) 쿼리스트링 파싱
        banks     = request.query_params.getlist('banks')
        calcType  = request.query_params.get('calcType', '')
        term      = request.query_params.get('term', '')
        joinWay   = request.query_params.get('joinWay', '')
        sortBy    = request.query_params.get('sortBy', 'kor_co_nm')
        sortOrder = request.query_params.get('sortOrder', 'asc')

        # 2) 금감원 적금 API 호출
        url = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
        params = {
            "auth": settings.FINLIFE_API_KEY,
            "topFinGrpNo": "020000",
            "pageNo": "1"
        }
        try:
            resp = requests.get(url, params=params, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            return Response(
                {"error": "금감원 API 요청 실패", "detail": str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        data      = resp.json().get("result", {})
        base_list = data.get("baseList", [])

        # 3) 필터링 (은행)
        if banks:
            patterns = []
            for sel in banks:
                patterns += BANK_ALIAS.get(sel, [sel])
            base_list = [
                b for b in base_list
                if any(pat in b.get("kor_co_nm", "") for pat in patterns)
            ]
        # 4) 가입방식 필터
        if joinWay:
            base_list = [
                b for b in base_list
                if joinWay in b.get("join_way", "")
            ]
        # 5) 단리/복리, 만기 필터
        if calcType:
            base_list = [
                b for b in base_list
                if b.get("intr_rate_type_nm") == calcType
            ]
        if term:
            base_list = [
                b for b in base_list
                if b.get("save_trm") == term
            ]

        # 6) 상품코드별 최고 금리(intr_rate2)만 남기기
        best_map = {}
        for item in base_list:
            code = item["fin_prdt_cd"]
            rate2 = float(item.get("intr_rate2") or item.get("intr_rate") or 0)
            existing = best_map.get(code)
            if not existing or rate2 > float(existing.get("intr_rate2") or existing.get("intr_rate") or 0):
                best_map[code] = item
        final_list = list(best_map.values())

        # 7) 정렬
        key_map = {
            "kor_co_nm": "kor_co_nm",
            "basicRate": "intr_rate",
            "maxRate":   "intr_rate2"
        }
        sort_key = key_map.get(sortBy, "kor_co_nm")
        reverse = (sortOrder == "desc")

        def sort_val(x):
            v = x.get(sort_key)
            return float(v) if sort_key in ("intr_rate", "intr_rate2") else (v or "")

        final_list.sort(key=sort_val, reverse=reverse)

        # 8) 결과 반환
        return Response({"baseList": final_list}, status=status.HTTP_200_OK)


from accounts.serializers import FinancialProfileSerializer  # 상단에 추가

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_financial_profile(request):
    try:
        profile = FinancialProfile.objects.get(user=request.user)
        if profile.checklist_submitted:
            serializer = FinancialProfileSerializer(profile)
            return Response({
                "has_profile": True,
                "profile": serializer.data  # ✅ 핵심: 프론트에서 기대하는 구조
            })
        else:
            return Response({
                "has_profile": False,
                "profile": None
            })
    except FinancialProfile.DoesNotExist:
        return Response({
            "has_profile": False,
            "profile": None
        })



class RecommendProducts(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        income       = int(request.GET.get('monthly_income', 0))
        product_type = request.GET.get('type', 'all')
        term         = request.GET.get('term')

        profile = None
        if request.user.is_authenticated:
            try:
                profile = FinancialProfile.objects.get(user=request.user)
            except FinancialProfile.DoesNotExist:
                pass

        api_key  = settings.FINLIFE_API_KEY
        base_url = "http://finlife.fss.or.kr/finlifeapi/"
        endpoints = {
            'deposit': "depositProductsSearch.json",
            'saving':  "savingProductsSearch.json"
        }

        try:
            results = []
            for kind, endpoint in endpoints.items():
                if product_type != 'all' and product_type != kind:
                    continue

                resp = requests.get(
                    base_url + endpoint,
                    params={"auth": api_key, "topFinGrpNo": "020000", "pageNo": "1"},
                    timeout=5
                )
                resp.raise_for_status()
                data        = resp.json().get("result", {})
                base_list   = data.get("baseList", [])
                option_list = data.get("optionList", []) if kind == 'deposit' else []

                # 예금/적금 공통 처리
                items = []
                if kind == 'deposit':
                    # merge base/option as in DepositProductData...
                    base_map = {b["fin_prdt_cd"]: b for b in base_list}
                    for o in option_list:
                        code = o["fin_prdt_cd"]
                        b = base_map.get(code)
                        if not b or not o.get("intr_rate"):
                            continue
                        if term and o.get("save_trm") != term:
                            continue
                        items.append({
                            "id":             code,
                            "type":           kind,
                            "name":           f"{b['kor_co_nm']} - {b['fin_prdt_nm']}",
                            "interest_rate":  float(o["intr_rate"]),
                            "term":           o.get("save_trm"),
                            "etc_note":       b.get("etc_note", ""),
                            "score":          0
                        })
                else:  # saving
                    for b in base_list:
                        if not b.get("intr_rate"):
                            continue
                        if term and b.get("save_trm") != term:
                            continue
                        items.append({
                            "id":             b["fin_prdt_cd"],
                            "type":           kind,
                            "name":           f"{b['kor_co_nm']} - {b['fin_prdt_nm']}",
                            "interest_rate":  float(b["intr_rate"]),
                            "term":           b.get("save_trm"),
                            "etc_note":       b.get("etc_note", ""),
                            "score":          0
                        })

                # 스코어 계산
                for prod in items:
                    prod["score"] = calculate_score(prod, profile)
                results.extend(items)

            # 점수 상위 3개
            top3 = sorted(results, key=lambda x: x["score"], reverse=True)[:3]
            return Response(top3)

        except Exception as e:
            return Response({"error": "추천 상품 로드 실패", "detail": str(e)}, status=500)


def calculate_score(product, profile):
    score = product["interest_rate"] * 40
    note  = product.get("etc_note", "").lower()
    ptype = product["type"]

    # 조건 편의성
    score += -20 if ("급여이체" in note or "우대" in note) else 30

    # 사용자 성향
    if profile:
        if profile.saving_style == "보수적" and ptype == "deposit":
            score += 30
        if profile.saving_style == "공격적" and ptype == "saving":
            score += product["interest_rate"] * 10
        if profile.spending_style == "공격적" and "우대" not in note:
            score += 10

    return score
