# backend/education/apps.py

import os
from django.apps import AppConfig

class EducationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'education'

    def ready(self):
        # runserver의 메인 프로세스(RUN_MAIN)에서만 실행
        if os.environ.get('RUN_MAIN') == 'true':
            from django.core.management import call_command
            from .models import FinanceTerm

            # 1) 금융 용어 fixtures 자동 로드 (비어 있을 때만)
            try:
                if not FinanceTerm.objects.exists():
                    call_command('loaddata', 'finance_terms.json', verbosity=0)
            except Exception:
                pass  # 이미 로드되었거나 개발 모드 에러 무시

            # 2) 최신 금융 뉴스 자동 크롤링
            try:
                call_command('fetch_news', verbosity=0)
            except Exception:
                pass  # 크롤링 실패시에도 서버 실행은 계속
