# backend/education/apps.py

from django.apps import AppConfig
import os
import sys
import time

# 모듈 레벨에 job 함수 정의 (APScheduler에서 직렬화 가능)
def fetch_finance_articles_job():
    from django.core.management import call_command
    call_command('fetch_finance_articles')

class EducationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'education'

    def ready(self):
        # runserver로 시작하는 경우에만 실행 (reload 중복 방지)
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') == 'true':
            # Django ORM 사용 전 필요한 import는 ready 내부로 이동
            from django.core.management import call_command
            from .models import QuizQuestion
            from django.conf import settings
            from apscheduler.schedulers.background import BackgroundScheduler
            from django_apscheduler.jobstores import DjangoJobStore
            from apscheduler.triggers.cron import CronTrigger

            # === 기존 크롤러 실행 ===
            print("======[서버 구동시 최신 금융 뉴스 수집 시작]======")
            t0 = time.time()
            try:
                call_command('fetch_finance_articles')
            except Exception as e:
                print(f"[EducationConfig] 크롤링 중 오류 발생: {e}")
            print(f"======[금융 뉴스 수집 완료] (소요: {time.time()-t0:.1f}초)======")

            # === 퀴즈 자동 로드 ===
            try:
                if not QuizQuestion.objects.exists():
                    quiz_fixture = os.path.join(settings.BASE_DIR, 'education', 'fixtures', 'finance_quiz.json')
                    print("======[퀴즈 데이터 자동 로드 시작]======")
                    call_command('loaddata', quiz_fixture, verbosity=0)
                    print("======[퀴즈 데이터 로드 완료]======")
                else:
                    print("🔁 퀴즈 데이터는 이미 존재하여 로드 생략")
            except Exception as e:
                print(f"[EducationConfig] 퀴즈 데이터 로드 중 오류 발생: {e}")

            # === APScheduler 설정 ===
            scheduler = BackgroundScheduler()
            scheduler.add_jobstore(DjangoJobStore(), 'default')

            # 매분 fetch_finance_articles 실행
            scheduler.add_job(
                func=fetch_finance_articles_job,
                trigger=CronTrigger(minute='*'),
                id='fetch_finance_articles_job',
                max_instances=1,
                replace_existing=True,
            )
            scheduler.start()
            print("======[APScheduler 시작: 매분 fetch_finance_articles 스케줄 등록]======")
