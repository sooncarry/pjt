# stock/apps.py

from django.apps import AppConfig
import os
import sys
import certifi
from django.core.management import call_command
from django.conf import settings

# ✅ 인증서 경로 설정 (SSL 문제 방지)
os.environ['SSL_CERT_FILE'] = certifi.where()

class StockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock'

    def ready(self):
        # runserver로 실행된 경우에만 동작
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') == 'true':
            try:
                # 📈 주식 지식 데이터 로드 시작 알림
                print("======[📈 주식 지식 데이터 loaddata 시작]======")

                fixtures_dir = os.path.join(
                    settings.BASE_DIR, 'stock', 'fixtures'
                )
                # 로드할 JSON 파일명을 나열
                fixtures = [
                    'stock_knowledge.json',
                ]

                for fixture_name in fixtures:
                    fixture_path = os.path.join(fixtures_dir, fixture_name)
                    if os.path.exists(fixture_path):
                        # verbosity=0 으로 로드 시 출력 억제
                        call_command('loaddata', fixture_path, verbosity=0)
                        print(f"======[✅ {fixture_name} 로드 완료]======")
                    else:
                        print(f"⚠️ {fixture_name} 파일이 없어 스킵합니다.")

            except Exception as e:
                print(f"[StockConfig] 주식 지식 로드 중 오류 발생: {e}")
