# savings/apps.py
import os
from django.apps import AppConfig
from django.core.management import call_command
from django.db.utils import OperationalError, ProgrammingError

class SavingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "savings"

    def ready(self):
        """
        runserver 시 ChallengeTemplate 테이블이 비어 있으면
        fixtures/templates.json을 자동으로 load.
        ─ 개발 편의용이므로 운영 배포 전에는 끄거나 B안을 추천.
        """
        # runserver의 자동 리로드로 중복 실행되는 것 방지
        if os.environ.get("RUN_MAIN") != "true":  
            return

        try:
            from savings.models import ChallengeTemplate
            # 이미 데이터가 있으면 스킵
            if ChallengeTemplate.objects.exists():
                return
            # 빈 경우에만 fixtures 로드
            call_command("loaddata", "templates.json", app_label="savings", verbosity=0)
            print("[savings] templates.json fixture loaded ✅")
        except (OperationalError, ProgrammingError):
            # 마이그레이션 직후 테이블이 없을 때 등을 무시
            pass
