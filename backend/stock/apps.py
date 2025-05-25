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
        # ✅ runserver로 실행된 경우에만 작동
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') == 'true':
            try:
                from .models import StockKnowledge
                if not StockKnowledge.objects.exists():
                    print("======[📈 주식 지식 데이터 로드 시작]======")
                    fixture_path = os.path.join(settings.BASE_DIR, 'stock', 'fixtures', 'stock_knowledge.json')


                    call_command('loaddata', fixture_path, verbosity=0)
                    print("======[✅ 주식 지식 데이터 로드 완료]======")
                else:
                    print("🔁 주식 지식 데이터는 이미 존재하여 로드 생략")
            except Exception as e:
                print(f"[StockConfig] 주식 지식 로드 중 오류 발생: {e}")
