import os
import zipfile
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from django.conf import settings

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_PATH = os.path.join(BASE_DIR, 'CORPCODE.zip')
XML_PATH = os.path.join(BASE_DIR, 'CORPCODE.xml')
CSV_PATH = os.path.join(BASE_DIR, 'corp_codes.csv')

# ✅ 1. CORPCODE.zip 다운로드 (ZIP 확인은 b'PK'로)
def download_corpcode_zip():
    api_key = settings.DART_API_KEY
    if not api_key:
        raise ValueError("환경변수 DART_API_KEY가 설정되어 있지 않습니다.")

    url = f'https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={api_key}'
    print(f"🔽 요청 URL: {url}")
    response = requests.get(url)

    print("🧪 응답 상태코드:", response.status_code)
    print("🧪 응답 Content-Type:", response.headers.get('Content-Type'))

    # ✅ 응답 내용 앞부분으로 ZIP 여부 확인
    if response.status_code == 200 and b'PK' in response.content[:10]:
        with open(ZIP_PATH, 'wb') as f:
            f.write(response.content)
        print(f"✅ CORPCODE.zip 저장 완료: {ZIP_PATH}")
    else:
        print("❌ 다운로드 실패")
        print("응답 본문 일부:", response.text[:300])

# ✅ 2. XML → CSV 파싱 및 저장
def download_and_parse_corp_code():
    if not os.path.exists(ZIP_PATH):
        print("❗ CORPCODE.zip이 없습니다. 먼저 download_corpcode_zip() 실행하세요.")
        return

    print("📦 CORPCODE.zip 압축 해제 중...")
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(BASE_DIR)

    print("📄 XML 파싱 중...")
    tree = ET.parse(XML_PATH)
    root = tree.getroot()

    corp_list = []
    for child in root:
        corp_code = child.find('corp_code').text.strip().zfill(8)
        corp_name = child.find('corp_name').text.strip()
        stock_code = child.find('stock_code').text.strip()
        corp_list.append({
            'corp_name': corp_name,
            'corp_code': corp_code,
            'stock_code': stock_code,
        })

    df = pd.DataFrame(corp_list)
    df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')
    print(f"✅ CSV 저장 완료: {CSV_PATH}")

# ✅ 3. 기업명 → corp_code (8자리 문자열 반환)
def get_corp_code(company_name: str):
    if not os.path.exists(CSV_PATH):
        print("⚠️ CSV 파일이 없어 XML을 다시 파싱합니다.")
        download_and_parse_corp_code()

    df = pd.read_csv(CSV_PATH, dtype=str)

    # ✅ 정확히 일치한 경우 우선 반환
    exact_match = df[df['corp_name'] == company_name]
    if not exact_match.empty:
        return exact_match.iloc[0]['corp_code'].zfill(8)

    # ✅ 그래도 없으면 contains 검색 (유사검색)
    fuzzy_match = df[df['corp_name'].str.contains(company_name, na=False)]
    if not fuzzy_match.empty:
        return fuzzy_match.iloc[0]['corp_code'].zfill(8)

    return None