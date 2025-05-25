# education/apps.py

from django.apps import AppConfig
import os, sys, time

class EducationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'education'

    def ready(self):
        # runserver로 시작하는 경우에만 실행 (reload 중복 방지)
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') == 'true':
            from django.core.management import call_command
            print("======[서버 구동시 최신 금융 뉴스 수집 시작]======")
            t0 = time.time()
            try:
                call_command('fetch_finance_articles')
            except Exception as e:
                print(f"[EducationConfig] 크롤링 중 오류 발생: {e}")
            print(f"======[금융 뉴스 수집 완료] (소요: {time.time()-t0:.1f}초)======")
